#!/usr/bin/env python3
# encoding: utf-8

from __future__ import annotations

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__version__ = (0, 0, 5)
__all__ = ["check_response", "P123Client", "P123OSError"]

from collections.abc import (
    AsyncIterable, Awaitable, Buffer, Callable, Coroutine, ItemsView, 
    Iterable, Iterator, Mapping, MutableMapping, Sized, 
)
from errno import EIO, EISDIR, ENOENT
from functools import partial
from hashlib import md5
from http.cookiejar import CookieJar
from inspect import isawaitable
from itertools import chain
from os import fsdecode, fstat, PathLike
from os.path import basename
from platform import system
from re import compile as re_compile
from tempfile import TemporaryFile
from typing import cast, overload, Any, Literal, Self
from uuid import uuid4
from warnings import filterwarnings

from aiofile import async_open
from asynctools import ensure_async
from property import locked_cacheproperty
from hashtools import file_digest, file_digest_async
from http_request import encode_multipart_data, encode_multipart_data_async
from iterutils import run_gen_step
from filewrap import (
    bio_chunk_iter, bio_chunk_async_iter, 
    bytes_iter_to_reader, bytes_iter_to_async_reader, 
    copyfileobj, copyfileobj_async, SupportsRead, 
)
from http_request import SupportsGeturl
from yarl import URL


# 当前的系统平台
SYS_PLATFORM = system()
# 替换表，用于半角转全角，包括了 Windows 中不允许出现在文件名中的字符
match SYS_PLATFORM:
    case "Windows":
        NAME_TANSTAB_FULLWIDH = {c: chr(c+65248) for c in b"\\/:*?|><"}
    case "Darwin":
        NAME_TANSTAB_FULLWIDH = {ord("/"): ":", ord(":"): "："}
    case _:
        NAME_TANSTAB_FULLWIDH = {ord("/"): "／"}
# 查找大写字母（除了左边第 1 个）
CRE_UPPER_ALPHABET_sub = re_compile("(?<!^)[A-Z]").sub
# 默认使用的域名
DEFAULT_BASE_URL = "https://www.123pan.com/b"
DEFAULT_LOGIN_BASE_URL = "https://login.123pan.com"
DEFAULT_OPEN_BASE_URL = "https://open-api.123pan.com"
# 默认的请求函数
_httpx_request = None

filterwarnings("ignore", category=SyntaxWarning)


class P123OSError(OSError):
    ...


def get_default_request():
    global _httpx_request
    if _httpx_request is None:
        from httpx_request import request
        _httpx_request = partial(request, timeout=(5, 60, 60, 5))
    return _httpx_request


def default_parse(resp, content: Buffer, /):
    from orjson import loads
    if isinstance(content, (bytes, bytearray, memoryview)):
        return loads(content)
    else:
        return loads(memoryview(content))


def buffer_length(b: Buffer, /) -> int:
    if isinstance(b, Sized):
        return len(b)
    else:
        return len(memoryview(b))


def items[K, V](
    m: Mapping[K, V] | Iterable[tuple[K, V]], 
    /, 
) -> Iterable[tuple[K, V]]:
    if isinstance(m, Mapping):
        try:
            get_items = getattr(m, "items")
            if isinstance((items := get_items()), ItemsView):
                return items
        except Exception:
            pass
        return ItemsView(m)
    return m


def dict_to_lower[K, V](
    d: Mapping[K, V] | Iterable[tuple[K, V]], 
    /, 
    *ds: Mapping[K, V] | Iterable[tuple[K, V]], 
    **kwd, 
) -> dict[K, V]:
    return {
        (k.lower() if isinstance(k, str) else k): v # type: ignore
        for k, v in cast(Iterator[tuple[K, V]], chain(items(d), *map(items, ds), kwd.items()))
    }


def dict_to_lower_merge[K, V](
    d: Mapping[K, V] | Iterable[tuple[K, V]], 
    /, 
    *ds: Mapping[K, V] | Iterable[tuple[K, V]], 
    **kwd, 
) -> dict[K, V]:
    m: dict[K, V] = {}
    setdefault = m.setdefault
    for k, v in cast(Iterator[tuple[K, V]], chain(items(d), *map(items, ds), kwd.items())):
        if isinstance(k, str):
            k = k.lower() # type: ignore
        setdefault(k, v)
    return m


@overload
def check_response(resp: dict, /) -> dict:
    ...
@overload
def check_response(resp: Awaitable[dict], /) -> Coroutine[Any, Any, dict]:
    ...
def check_response(resp: dict | Awaitable[dict], /) -> dict | Coroutine[Any, Any, dict]:
    """检测 123 的某个接口的响应，如果成功则直接返回，否则根据具体情况抛出一个异常，基本上是 OSError 的实例
    """
    def check(resp, /) -> dict:
        if not isinstance(resp, dict) or resp.get("code", 0) not in (0, 200):
            raise P123OSError(EIO, resp)
        return resp
    if isawaitable(resp):
        async def check_await() -> dict:
            return check(await resp)
        return check_await()
    else:
        return check(resp)


class P123Client:

    def __init__(
        self, 
        /, 
        passport: int | str = "", 
        password: str = "", 
        token: str = "", 
    ):
        self.passport = passport
        self.password = password
        self.token = token
        if passport and password:
            self.login()

    def __del__(self, /):
        self.close()

    @property
    def cookies(self, /):
        """请求所用的 Cookies 对象（同步和异步共用）
        """
        try:
            return self.__dict__["cookies"]
        except KeyError:
            from httpx import Cookies
            cookies = self.__dict__["cookies"] = Cookies()
            return cookies

    @property
    def cookiejar(self, /) -> CookieJar:
        """请求所用的 CookieJar 对象（同步和异步共用）
        """
        return self.cookies.jar

    @property
    def headers(self, /) -> MutableMapping:
        """请求头，无论同步还是异步请求都共用这个请求头
        """
        try:
            return self.__dict__["headers"]
        except KeyError:
            from multidict import CIMultiDict
            headers = self.__dict__["headers"] = CIMultiDict({
                "accept": "*/*", 
                "accept-encoding": "gzip, deflate", 
                "app-version": "3", 
                "connection": "keep-alive", 
                "platform": "web", 
                "user-agent": "Mozilla/5.0 AppleWebKit/600 Safari/600 Chrome/124.0.0.0 Edg/124.0.0.0", 
            })
            return headers

    @locked_cacheproperty
    def session(self, /):
        """同步请求的 session 对象
        """
        import httpx_request
        from httpx import Client, HTTPTransport, Limits
        session = Client(
            limits=Limits(max_connections=256, max_keepalive_connections=64, keepalive_expiry=10), 
            transport=HTTPTransport(retries=5), 
            verify=False, 
        )
        setattr(session, "_headers", self.headers)
        setattr(session, "_cookies", self.cookies)
        return session

    @locked_cacheproperty
    def async_session(self, /):
        """异步请求的 session 对象
        """
        import httpx_request
        from httpx import AsyncClient, AsyncHTTPTransport, Limits
        session = AsyncClient(
            limits=Limits(max_connections=256, max_keepalive_connections=64, keepalive_expiry=10), 
            transport=AsyncHTTPTransport(retries=5), 
            verify=False, 
        )
        setattr(session, "_headers", self.headers)
        setattr(session, "_cookies", self.cookies)
        return session

    @property
    def token(self, /) -> str:
        return self._token

    @token.setter
    def token(self, value: str, /):
        self._token = value
        if value:
            self.headers["authorization"] = f"Bearer {self._token}"
        else:
            self.headers.pop("authorization", None)

    @token.deleter
    def token(self, /):
        self.token = ""

    def close(self, /) -> None:
        """删除 session 和 async_session 属性，如果它们未被引用，则应该会被自动清理
        """
        self.__dict__.pop("session", None)
        self.__dict__.pop("async_session", None)

    @overload
    def login(
        self, 
        /, 
        passport: int | str = "", 
        password: str = "", 
        remember: bool = True, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> Self:
        ...
    @overload
    def login(
        self, 
        /, 
        passport: int | str = "", 
        password: str = "", 
        remember: bool = True, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, Self]:
        ...
    def login(
        self, 
        /, 
        passport: int | str = "", 
        password: str = "", 
        remember: bool = True, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> Self | Coroutine[Any, Any, Self]:
        if passport:
            self.passport = passport
        else:
            passport = self.passport
        if password:
            self.password = password
        else:
            password = self.password
        def gen_step():
            if passport and password:
                resp = yield self.user_login(
                    {"passport": passport, "password": password, "remember": remember}, 
                    base_url=base_url, 
                    async_=async_, 
                    **request_kwargs, 
                )
                check_response(resp)
                self.token = resp["data"]["token"]
            return self
        return run_gen_step(gen_step, async_=async_)

    def request(
        self, 
        /, 
        url: str, 
        method: str = "POST", 
        request: None | Callable = None, 
        base_url: str = "", 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ):
        """执行 HTTP 请求，默认为 POST 方法
        """
        if url.startswith("//"):
            url = "https:" + url
        elif not url.startswith(("http://", "https://")):
            if not url.startswith("/"):
                url = "/api/" + url
            url = (base_url or DEFAULT_BASE_URL) + url
        request_kwargs.setdefault("parse", default_parse)
        if request is None:
            request_kwargs["session"] = self.async_session if async_ else self.session
            return get_default_request()(
                url=url, 
                method=method, 
                async_=async_, 
                **request_kwargs, 
            )
        else:
            if headers := request_kwargs.get("headers"):
                request_kwargs["headers"] = {**self.headers, **headers}
            else:
                request_kwargs["headers"] = self.headers
            return request(
                url=url, 
                method=method, 
                **request_kwargs, 
            )

    @overload
    @staticmethod
    def app_dydomain(
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def app_dydomain(
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def app_dydomain(
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取 123 网盘的各种域名

        GET https://www.123pan.com/api/dydomain
        """
        api = f"{base_url or DEFAULT_BASE_URL}/api/dydomain"
        request_kwargs.setdefault("parse", default_parse)
        if request is None:
            return get_default_request()(url=api, method="GET", async_=async_, **request_kwargs)
        else:
            return request(url=api, method="GET", **request_kwargs)

    @overload
    def download_info(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def download_info(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def download_info(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取下载信息

        POST https://www.123pan.com/api/file/download_info

        .. hint::
            即使文件已经被删除，只要还有 S3KeyFlag 和 Etag （即 MD5） 就依然可以下载

            你完全可以构造这样的查询参数

            .. code:: python

                payload = {
                    "Etag": "...",   # 必填，文件的 MD5
                    "FileID": 0,     # 可以随便填
                    "FileName": "a", # 随便填一个名字
                    "S3KeyFlag": str # 必填，格式为 f"{UID}-0"，UID 就是上传此文件的用户的 UID，如果此文件是由你上传的，则可从 `P123Client.user_info` 的响应中获取
                    "Size": 0,       # 可以随便填，填了可能搜索更准确
                }

        .. note::
            获取的直链有效期是 24 小时

        :payload:
            - Etag: str 💡 文件的 MD5 散列值
            - S3KeyFlag: str
            - FileName: str = <default> 💡 默认用 Etag（即 MD5）作为文件名
            - FileID: int | str = 0
            - Size: int = <default>
            - Type: int = 0
            - driveId: int | str = 0
            - ...
        """
        api = "file/download_info"
        def gen_step():
            nonlocal payload
            if headers := request_kwargs.get("headers"):
                headers = dict(headers)
            else:
                headers = {}
            headers["platform"] = "android"
            request_kwargs["headers"] = headers
            if not isinstance(payload, dict):
                resp = yield self.fs_info(payload, base_url=base_url, async_=async_, **request_kwargs)
                resp["payload"] = payload
                check_response(resp)
                info_list = resp["data"]["infoList"]
                if not info_list:
                    raise FileNotFoundError(ENOENT, resp)
                payload = cast(dict, info_list[0])
                if payload["Type"]:
                    raise IsADirectoryError(EISDIR, resp)
            payload = dict_to_lower_merge(payload, {"driveId": 0, "Type": 0, "FileID": 0})
            if "filename" not in payload:
                payload["filename"] = payload["etag"]
            return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)
        return run_gen_step(gen_step, async_=async_)

    @overload
    def download_info_batch(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def download_info_batch(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def download_info_batch(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取批量下载信息

        POST https://www.123pan.com/api/file/batch_download_info

        .. warning::
            会把一些文件或目录以 zip 包的形式下载，但非会员有流量限制，所以还是推荐用 `P123Client.download_info` 逐个获取下载链接并下载

        :payload:
            - fileIdList: list[FileID]

                .. code:: python

                    FileID = {
                        "FileId": int | str
                    }
        """
        api = "api/file/batch_download_info"
        if isinstance(payload, (int, str)):
            payload = {"fileIdList": [{"FileId": payload}]}
        elif not isinstance(payload, dict):
            payload = {"fileIdList": [{"FileId": fid} for fid in payload]}
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_copy(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_copy(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_copy(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """复制

        POST https://www.123pan.com/api/restful/goapi/v1/file/copy/async

        :payload:
            - fileList: list[File] 💡 信息可以取自 `P123Client.fs_info` 接口

                .. code:: python

                    File = { 
                        "FileId": int | str, 
                        ...
                    }

            - targetFileId: int | str = 0
        """
        api = "restful/goapi/v1/file/copy/async"
        def gen_step():
            nonlocal payload
            if not isinstance(payload, dict):
                resp = yield self.fs_info(payload, base_url=base_url, async_=async_, **request_kwargs)
                resp["payload"] = payload
                check_response(resp)
                info_list = resp["data"]["infoList"]
                if not info_list:
                    raise FileNotFoundError(ENOENT, resp)
                payload = {"fileList": info_list}
            payload = dict_to_lower_merge(payload, targetFileId=parent_id)
            return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)
        return run_gen_step(gen_step, async_=async_)

    @overload
    def fs_detail(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_detail(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_detail(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件或目录详情（文件数、目录数、总大小）

        GET https://www.123pan.com/api/file/detail

        :payload:
            - fileID: int | str
        """
        api = "file/detail"
        if isinstance(payload, (int, str)):
            payload = {"fileID": payload}
        return self.request(url=api, method="GET", params=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_delete(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_delete(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_delete(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """彻底删除

        POST https://www.123pan.com/api/file/delete

        .. hint::
            彻底删除文件前,文件必须要在回收站中,否则无法删除

        :payload:
            - fileIdList: list[FileID]

                .. code:: python

                    FileID = {
                        "FileId": int | str
                    }

            - event: str = "recycleDelete"
        """
        api = "file/delete"
        if isinstance(payload, (int, str)):
            payload = {"fileIdList": [{"FileId": payload}]}
        elif not isinstance(payload, dict):
            payload = {"fileIdList": [{"FileId": fid} for fid in payload]}
        payload = cast(dict, payload)
        payload.setdefault("event", "recycleDelete")
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_get_path(
        self, 
        payload: int | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_get_path(
        self, 
        payload: int | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_get_path(
        self, 
        payload: int | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取某个 id 对应的祖先节点列表

        POST https://www.123pan.com/api/file/get_path

        :payload:
            - fileId: int 💡 文件 id
        """
        api = "file/get_path"
        if isinstance(payload, int):
            payload = {"fileId": payload}
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_info(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_info(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_info(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件信息

        POST https://www.123pan.com/api/file/info

        :payload:
            - fileIdList: list[FileID]

                .. code:: python

                    FileID = {
                        "FileId": int | str
                    }
        """
        api = "file/info"
        if isinstance(payload, (int, str)):
            payload = {"fileIdList": [{"FileId": payload}]}
        elif not isinstance(payload, dict):
            payload = {"fileIdList": [{"FileId": fid} for fid in payload]}
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_list(
        self, 
        payload: int | str | dict = 0, 
        /, 
        event: str = "homeListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_list(
        self, 
        payload: int | str | dict = 0, 
        /, 
        event: str = "homeListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_list(
        self, 
        payload: int | str | dict = 0, 
        /, 
        event: str = "homeListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件列表（可搜索）

        GET https://www.123pan.com/api/file/list

        .. note::
            如果返回信息中，有 "Next" 的值为 "-1"，说明无下一页

        :payload:
            - driveId: int | str = 0
            - limit: int = 100 💡 分页大小，最大不超过100
            - next: int = 0    💡 下一批拉取开始的 id
            - orderBy: str = "file_id" 💡 排序依据："file_id", "file_name", "create_at", "update_at", "size", "share_id", ...
            - orderDirection: "asc" | "desc" = "asc" 💡 排序顺序
            - Page: int = <default> 💡 第几页，从 1 开始，可以是 0
            - parentFileId: int | str = 0 💡 父目录 id
            - trashed: "false" | "true" = <default> 💡 是否查看回收站的文件
            - inDirectSpace: "false" | "true" = "false"
            - event: str = "homeListFile" 💡 事件名称

                - "homeListFile": 全部文件
                - "recycleListFile": 回收站
                - "syncFileList": 同步空间

            - operateType: int | str = <default> 💡 操作类型，如果在同步空间，则需要指定为 "SyncSpacePage"
            - SearchData: str = <default> 💡 搜索关键字（将无视 `parentFileId` 参数）
            - OnlyLookAbnormalFile: int = <default>
        """
        api = "file/list"
        if isinstance(payload, (int, str)):
            payload = {"parentFileId": payload}
        payload = dict_to_lower_merge(payload, {
            "driveId": 0, 
            "limit": 100, 
            "next": 0, 
            "orderBy": "file_id", 
            "orderDirection": "asc", 
            "parentFileId": 0, 
            "inDirectSpace": "false", 
            "event": event, 
        })
        if not payload.get("trashed"):
            match payload["event"]:
                case "recycleListFile":
                    payload["trashed"] = "true"
                case _:
                    payload["trashed"] = "false"
        return self.request(url=api, method="GET", params=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_list_new(
        self, 
        payload: int | str | dict = 0, 
        /, 
        event: str = "homeListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_list_new(
        self, 
        payload: int | str | dict = 0, 
        /, 
        event: str = "homeListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_list_new(
        self, 
        payload: int | str | dict = 0, 
        /, 
        event: str = "homeListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件列表（可搜索）

        GET https://www.123pan.com/api/file/list/new

        .. note::
            如果返回信息中，有 "Next" 的值为 "-1"，说明无下一页

        :payload:
            - driveId: int | str = 0
            - limit: int = 100 💡 分页大小，最大不超过100
            - next: int = 0    💡 下一批拉取开始的 id
            - orderBy: str = "file_id" 💡 排序依据："file_id", "file_name", "create_at", "update_at", "size", "share_id", ...
            - orderDirection: "asc" | "desc" = "asc" 💡 排序顺序
            - Page: int = <default> 💡 第几页，从 1 开始，可以是 0
            - parentFileId: int | str = 0 💡 父目录 id
            - trashed: "false" | "true" = <default> 💡 是否查看回收站的文件
            - inDirectSpace: "false" | "true" = "false"
            - event: str = "homeListFile" 💡 事件名称

                - "homeListFile": 全部文件
                - "recycleListFile": 回收站
                - "syncFileList": 同步空间

            - operateType: int | str = <default> 💡 操作类型，如果在同步空间，则需要指定为 "SyncSpacePage"
            - SearchData: str = <default> 💡 搜索关键字（将无视 `parentFileId` 参数）
            - OnlyLookAbnormalFile: int = <default>
        """
        api = "file/list/new"
        if isinstance(payload, (int, str)):
            payload = {"parentFileId": payload}
        payload = dict_to_lower_merge(payload, {
            "driveId": 0, 
            "limit": 100, 
            "next": 0, 
            "orderBy": "file_id", 
            "orderDirection": "asc", 
            "parentFileId": 0, 
            "inDirectSpace": "false", 
            "event": event, 
        })
        if not payload.get("trashed"):
            match payload["event"]:
                case "recycleListFile":
                    payload["trashed"] = "true"
                case _:
                    payload["trashed"] = "false"
        return self.request(url=api, method="GET", params=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_mkdir(
        self, 
        name: str, 
        /, 
        parent_id: int | str = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_mkdir(
        self, 
        name: str, 
        /, 
        parent_id: int | str = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_mkdir(
        self, 
        name: str, 
        /, 
        parent_id: int | str = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """创建目录

        :param name: 目录名
        :param parent_id: 父目录 id
        :param duplicate: 处理同名：0: 复用 1: 保留两者 2: 替换
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数

        :return: 接口响应
        """
        payload = {"filename": name, "parentFileId": parent_id}
        if duplicate:
            payload["NotReuse"] = True
            payload["duplicate"] = duplicate
        return self.upload_request(payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_move(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_move(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_move(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """移动

        POST https://www.123pan.com/api/file/mod_pid

        :payload:
            - fileIdList: list[FileID]

                .. code:: python

                    FileID = {
                        "FileId": int | str
                    }

            - parentFileId: int | str = 0
            - event: str = "fileMove"
        """
        api = "file/mod_pid"
        if isinstance(payload, (int, str)):
            payload = {"fileIdList": [{"FileId": payload}]}
        elif not isinstance(payload, dict):
            payload = {"fileIdList": [{"FileId": fid} for fid in payload]}
        payload = dict_to_lower_merge(payload, {"parentFileId": parent_id, "event": "fileMove"})
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_rename(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_rename(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_rename(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """（单个）改名

        POST https://www.123pan.com/api/file/rename

        :payload:
            - FileId: int | str
            - fileName: str
            - driveId: int | str = 0
            - duplicate: 0 | 1 | 2 = 0 💡 处理同名：0: 提示/忽略 1: 保留两者 2: 替换
            - event: str = "fileRename"
        """
        api = "file/rename"
        payload = dict_to_lower_merge(payload, {
            "driveId": 0, 
            "duplicate": 0, 
            "event": "fileRename", 
        })
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_trash(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        event: str = "intoRecycle", 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_trash(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        event: str = "intoRecycle", 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_trash(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        event: str = "intoRecycle", 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """操作回收站

        POST https://www.123pan.com/api/file/trash

        :payload:
            - fileTrashInfoList: list[File] 💡 信息可以取自 `P123Client.fs_info` 接口

                .. code:: python

                    File = { 
                        "FileId": int | str, 
                        ...
                    }

            - driveId: int = 0
            - event: str = "intoRecycle" 💡 事件类型

                - "intoRecycle": 移入回收站
                - "recycleRestore": 移出回收站

            - operation: bool = <default>
        """
        api = "file/trash"
        if isinstance(payload, (int, str)):
            payload = {"fileTrashInfoList": [{"FileId": payload}]}
        elif not isinstance(payload, dict):
            payload = {"fileTrashInfoList": [{"FileId": fid} for fid in payload]}
        payload = dict_to_lower_merge(payload, {"driveId": 0, "event": event})
        if payload.get("operation") is None:
            match payload["event"]:
                case "recycleRestore":
                    payload["operation"] = False
                case _:
                    payload["operation"] = True
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def fs_trash_clear(
        self, 
        payload: dict = {"event": "recycleClear"}, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_trash_clear(
        self, 
        payload: dict = {"event": "recycleClear"}, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_trash_clear(
        self, 
        payload: dict = {"event": "recycleClear"}, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """清空回收站

        POST https://www.123pan.com/api/file/trash_delete_all

        :payload:
            - event: str = "recycleClear"
        """
        api = "file/trash_delete_all"
        payload.setdefault("event", "recycleClear")
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def offline_task_delete(
        self, 
        payload: int | Iterable[int] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_task_delete(
        self, 
        payload: int | Iterable[int] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_task_delete(
        self, 
        payload: int | Iterable[int] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除离线下载任务

        POST https://www.123pan.com/api/offline_download/task/delete

        :payload:
            - task_ids: list[int] 💡 任务 id 列表
            - status_arr: list[0|1|2] = [] 💡 状态列表：0:等待 1:运行 2:完成
        """
        api = "offline_download/task/delete"
        if isinstance(payload, int):
            payload = {"task_ids": [payload], "status_arr": []}
        elif not isinstance(payload, dict):
            if not isinstance(payload, (list, tuple)):
                payload = tuple(payload)
            payload = {"task_ids": payload, "status_arr": []}
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def offline_task_list(
        self, 
        payload: int | dict = 1, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_task_list(
        self, 
        payload: int | dict = 1, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_task_list(
        self, 
        payload: int | dict = 1, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """离线下载任务列表

        POST https://www.123pan.com/api/offline_download/task/list

        :payload:
            - current_page: int = 1
            - page_size: 100
            - status_arr: list[0|1|2] = [0, 1] 💡 状态列表：0:等待 1:运行 2:完成
        """
        api = "offline_download/task/list"
        if isinstance(payload, int):
            payload = {"current_page": payload, "page_size": 100, "status_arr": [0, 1]}
        else:
            payload = {"current_page": 1, "page_size": 100, "status_arr": [0, 1], **payload}
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def offline_task_resolve(
        self, 
        payload: str | Iterable[str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_task_resolve(
        self, 
        payload: str | Iterable[str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_task_resolve(
        self, 
        payload: str | Iterable[str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """解析下载链接

        POST https://www.123pan.com/api/offline_download/task/resolve

        :payload:
            - urls: str = <default> 💡 下载链接，多个用 "\n" 隔开（用于新建链接下载任务）
            - info_hash: str = <default> 💡 种子文件的 info_hash（用于新建BT任务）
        """
        api = "offline_download/task/resolve"
        if isinstance(payload, str):
            payload = {"urls": payload.strip("\n")}
        elif not isinstance(payload, dict):
            payload = {"urls": "\n".join(payload)}
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    # TODO: 支持接受一个 Iterable[int | dict]，int 视为 id （select_file 为 [0]），dict 视为 resolve 信息
    @overload
    def offline_task_submit(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_task_submit(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_task_submit(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """提交离线下载任务

        POST https://www.123pan.com/api/offline_download/task/submit

        :payload:
            - resource_list: list[Task] 💡 资源列表

                .. code:: python

                    File = {
                        "resource_id": int, 
                        "select_file": list[int] # 如果是链接下载，则传 [0]，如果BT下载，则传需要下载的文件在列表中的索引的列表
                    }

            - upload_dir: int 💡 保存到目录的 id
        """
        api = "offline_download/task/submit"
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def offline_task_upload_seed(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer], 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_task_upload_seed(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer], 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_task_upload_seed(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer], 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """上传种子，以作解析

        POST https://www.123pan.com/api/offline_download/upload/seed
        """
        api = "offline_download/upload/seed"
        if async_:
            headers, request_kwargs["data"] = encode_multipart_data_async({}, {"upload-torrent": file}, file_suffix=".torrent")
        else:
            headers, request_kwargs["data"] = encode_multipart_data({}, {"upload-torrent": file}, file_suffix=".torrent") # type: ignore
        request_kwargs["headers"] = {**(request_kwargs.get("headers") or {}), **headers}
        return self.request(url=api, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_cancel(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_cancel(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_cancel(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """取消分享

        POST https://www.123pan.com/api/share/delete

        :payload:
            - shareInfoList: list[ShareID] 💡 信息可以取自 `P123Client.fs_info` 接口

                .. code:: python

                    ShareID = { 
                        "shareId": int | str, 
                    }

            - driveId: int = 0
            - event: str = "shareCancel" 💡 事件类型
            - isPayShare: bool = False 💡 是否付费分享
        """
        api = "share/delete"
        if isinstance(payload, (int, str)):
            payload = {"shareInfoList": [{"shareId": payload}]}
        elif not isinstance(payload, dict):
            payload = {"shareInfoList": [{"shareId": sid} for sid in payload]}
        payload = dict_to_lower_merge(payload, {
            "driveId": 0, 
            "event": "shareCancel", 
            "isPayShare": False, 
        })
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_clear(
        self, 
        payload: dict = {"event": "shareClear"}, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_clear(
        self, 
        payload: dict = {"event": "shareClear"}, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_clear(
        self, 
        payload: dict = {"event": "shareClear"}, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """清理全部失效链接

        GET https://www.123pan.com/api/share/clean_expire

        :payload:
            - event: str = "shareClear"
        """
        api = "share/clean_expire"
        return self.request(url=api, method="GET", params=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_create(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_create(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_create(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """创建分享

        POST https://www.123pan.com/api/share/create

        :payload:
            - fileIdList: int | str 💡 文件或目录的 id，多个用逗号 "," 分隔
            - displayStatus: int = 2     💡 默认展示：1:平铺 2:列表
            - driveId: int = 0
            - event: str = "shareCreate" 💡 事件类型
            - expiration: "9999-12-31T23:59:59+08:00" 💡 有效期，日期用 ISO 格式
            - isPayShare: bool = False   💡 是否付费分享
            - isReward: 0 | 1 = 0        💡 是否开启打赏
            - payAmount: int = 0         💡 付费金额，单位：分
            - renameVisible: bool = False
            - resourceDesc: str = ""     💡 资源描述
            - shareName: str = <default> 💡 分享名称
            - sharePwd: str = ""         💡 分享密码
            - trafficLimit: int = 0      💡 流量限制额度，单位字节
            - trafficLimitSwitch: 1 | 2 = 1 💡 是否开启流量限制：1:关闭 2:开启
            - trafficSwitch: 1 | 2 = 1      💡 是否开启免登录流量包：1:关闭 2:开启
        """
        api = "share/create"
        if isinstance(payload, (int, str)):
            payload = {"fileIdList": payload}
        elif not isinstance(payload, dict):
            payload = {"fileIdList": ",".join(map(str, payload))}
        payload = dict_to_lower_merge(payload, {
            "displayStatus": 2, 
            "driveId": 0, 
            "event": "shareCreate", 
            "expiration": "9999-12-31T23:59:59+08:00", 
            "isPayShare": False, 
            "isReward": 0, 
            "payAmount": 0, 
            "renameVisible": False, 
            "resourceDesc": "", 
            "sharePwd": "", 
            "trafficLimit": 0, 
            "trafficLimitSwitch": 1, 
            "trafficSwitch": 1, 
        })
        if "fileidlist" not in payload:
            raise ValueError("missing field: 'fileIdList'")
        if "sharename" not in payload:
            payload["sharename"] = "%d 个文件或目录" % (str(payload["fileidlist"]).count(",") + 1)
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_download_info(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_download_info(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_download_info(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取分享中的下载信息

        POST https://www.123pan.com/api/share/download/info

        .. note::
            可以作为 staticmethod 使用，此时第 1 个位置参数要传入 None 或者 dict

            如果文件在 100MB 以内，下载时是不需要登录的；如果超过 100 MB，但分享者设置的免登录流量包未告罄，下载时也不需要登录

            你也可以使用 `P123Client.download_info` 来获取下载链接，则不需要提供 "ShareKey" 和 "SharePwd"

        :payload:
            - ShareKey: str 💡 分享码
            - SharePwd: str = <default> 💡 密码，如果没有就不用传
            - Etag: str
            - S3KeyFlag: str
            - FileID: int | str
            - Size: int = <default>
            - ...
        """
        if isinstance(self, dict):
            payload = self
            self = None
        assert payload is not None
        if headers := request_kwargs.get("headers"):
            headers = dict(headers)
        else:
            headers = {}
        headers["platform"] = "android"
        request_kwargs["headers"] = headers
        if self is None:
            api = f"{base_url or DEFAULT_BASE_URL}/api/share/download/info"
            request_kwargs.setdefault("parse", default_parse)
            request = request_kwargs.pop("request", None)
            if request is None:
                return get_default_request()(url=api, method="POST", json=payload, async_=async_, **request_kwargs)
            else:
                return request(url=api, method="POST", json=payload, **request_kwargs)
        else:
            api = "share/download/info"
            return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_download_info_batch(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_download_info_batch(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_download_info_batch(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取分享中的批量下载信息

        POST https://www.123pan.com/api/file/batch_download_share_info

        .. note::
            可以作为 staticmethod 使用，此时第 1 个位置参数要传入 None 或者 dict

        :payload:
            - ShareKey: str 💡 分享码
            - SharePwd: str = <default> 💡 密码，如果没有就不用传
            - fileIdList: list[FileID]

                .. code:: python

                    FileID = {
                        "FileId": int | str
                    }
        """
        if isinstance(self, dict):
            payload = self
            self = None
        assert payload is not None
        if self is None:
            api = f"{base_url or DEFAULT_BASE_URL}/api/file/batch_download_share_info"
            request_kwargs.setdefault("parse", default_parse)
            request = request_kwargs.pop("request", None)
            if request is None:
                return get_default_request()(url=api, method="POST", json=payload, async_=async_, **request_kwargs)
            else:
                return request(url=api, method="POST", json=payload, **request_kwargs)
        else:
            api = "file/batch_download_share_info"
            return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_fs_copy(
        self, 
        payload: dict, 
        /, 
        parent_id: None | int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_fs_copy(
        self, 
        payload: dict, 
        /, 
        parent_id: None | int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_fs_copy(
        self, 
        payload: dict, 
        /, 
        parent_id: None | int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """转存

        POST https://www.123pan.com/api/file/copy/async

        .. caution::
            这个函数的字段名，使用 snake case，而不是 camel case

        :payload:
            - share_key: str 💡 分享码
            - share_pwd: str = <default> 💡 密码，如果没有就不用传
            - current_level: int = 1
            - event: str = "transfer"
            - file_list: list[File]

                .. code:: python

                    File = {
                        "file_id": int | str, 
                        "file_name": str, 
                        "etag": str, 
                        "parent_file_id": int | str = 0, 
                        "drive_id": int | str = 0, 
                        ...
                    }
        """
        api = "file/copy/async"
        def to_snake_case(
            payload: dict[str, Any], 
            /, 
            mapping={
                "sharekey": "share_key", 
                "sharepwd": "share_pwd", 
                "filelist": "file_list", 
                "fileid": "file_id", 
                "filename": "file_name", 
                "parentfileid": "parent_file_id", 
                "driveid": "drive_id", 
                "currentlevel": "current_level", 
            }, 
        ):
            d: dict[str, Any] = {}
            for k, v in payload.items():
                if "_" in k:
                    d[k.lower()] = v
                elif k2 := mapping.get(k.lower()):
                    d[k2] = v
                elif (k2 := CRE_UPPER_ALPHABET_sub(r"_\g<0>", k)) != k:
                    d[k2.lower()] = v
                else:
                    d[k] = v
            if "file_list" in d:
                ls = d["file_list"]
                for i, d2 in enumerate(ls):
                    ls[i] = {"drive_id": 0, **to_snake_case(d2)}
                    if parent_id is not None:
                        ls[i]["parent_file_id"] = parent_id
            return d
        payload = {"current_level": 1, "event": "transfer", **to_snake_case(payload)}
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_fs_list(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_fs_list(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_fs_list(
        self: None | dict | P123Client = None, 
        payload: None | dict = None, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取分享中的文件列表

        GET https://www.123pan.com/api/share/get

        .. note::
            如果返回信息中，有 "Next" 的值为 "-1"，说明无下一页

        :payload:
            - ShareKey: str 💡 分享码
            - SharePwd: str = <default> 💡 密码，如果没有就不用传
            - limit: int = 100 💡 分页大小，最大不超过100
            - next: int = 0    💡 下一批拉取开始的 id
            - orderBy: str = "file_name" 💡 排序依据："file_name", "create_at", "update_at", "size", ...
            - orderDirection: "asc" | "desc" = "asc" 💡 排序顺序
            - Page: int = 1 💡 第几页，从 1 开始，可以是 0
            - parentFileId: int | str = 0 💡 父目录 id
            - event: str = "homeListFile" 💡 事件名称
            - operateType: int | str = <default> 💡 操作类型
        """
        if isinstance(self, dict):
            payload = self
            self = None
        assert payload is not None
        payload = dict_to_lower_merge(cast(dict, payload), {
            "limit": 100, 
            "next": 0, 
            "orderBy": "file_name", 
            "orderDirection": "asc", 
            "Page": 1, 
            "parentFileId": 0, 
            "event": "homeListFile", 
        })
        request_kwargs.setdefault("parse", default_parse)
        if self is None:
            api = f"{base_url or DEFAULT_BASE_URL}/api/share/get"
            if request is None:
                return get_default_request()(url=api, method="GET", params=payload, async_=async_, **request_kwargs)
            else:
                return request(url=api, method="GET", params=payload, **request_kwargs)
        else:
            api = "share/get"
            return self.request(url=api, method="GET", params=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_list(
        self, 
        payload: int | dict = 1, 
        /, 
        event: str = "shareListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_list(
        self, 
        payload: int | dict = 1, 
        /, 
        event: str = "shareListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_list(
        self, 
        payload: int | dict = 1, 
        /, 
        event: str = "shareListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取免费分享列表（可搜索）

        GET https://www.123pan.com/api/share/list

        .. note::
            如果返回信息中，有 "Next" 的值为 "-1"，说明无下一页

        :payload:
            - driveId: int | str = 0
            - limit: int = 100 💡 分页大小，最大不超过100
            - next: int = 0    💡 下一批拉取开始的 id
            - orderBy: str = "fileId" 💡 排序依据："fileId", ...
            - orderDirection: "asc" | "desc" = "desc" 💡 排序顺序
            - Page: int = <default> 💡 第几页，从 1 开始，可以是 0
            - event: str = "shareListFile"
            - operateType: int | str = <default>
            - SearchData: str = <default> 💡 搜索关键字（将无视 `parentFileId` 参数）
        """
        api = "share/list"
        if isinstance(payload, int):
            payload = {"Page": payload}
        payload = dict_to_lower_merge(payload, {
            "driveId": 0, 
            "limit": 100, 
            "next": 0, 
            "orderBy": "fileId", 
            "orderDirection": "desc", 
            "event": event, 
        })
        return self.request(url=api, method="GET", params=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_payment_list(
        self, 
        payload: int | dict = 1, 
        /, 
        event: str = "shareListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_payment_list(
        self, 
        payload: int | dict = 1, 
        /, 
        event: str = "shareListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_payment_list(
        self, 
        payload: int | dict = 1, 
        /, 
        event: str = "shareListFile", 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取付费分享列表（可搜索）

        GET https://www.123pan.com/api/restful/goapi/v1/share/content/payment/list

        .. note::
            如果返回信息中，有 "Next" 的值为 "-1"，说明无下一页

        :payload:
            - driveId: int | str = 0
            - limit: int = 100 💡 分页大小，最大不超过100
            - next: int = 0    💡 下一批拉取开始的 id
            - orderBy: str = "fileId" 💡 排序依据："fileId", ...
            - orderDirection: "asc" | "desc" = "desc" 💡 排序顺序
            - Page: int = <default> 💡 第几页，从 1 开始，可以是 0
            - event: str = "shareListFile"
            - operateType: int | str = <default>
            - SearchData: str = <default> 💡 搜索关键字（将无视 `parentFileId` 参数）
        """
        api = "restful/goapi/v1/share/content/payment/list"
        if isinstance(payload, int):
            payload = {"Page": payload}
        payload = dict_to_lower_merge(payload, {
            "driveId": 0, 
            "limit": 100, 
            "next": 0, 
            "orderBy": "fileId", 
            "orderDirection": "desc", 
            "event": event, 
        })
        return self.request(url=api, method="GET", params=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_reward_set(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        is_reward: bool = False, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_reward_set(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        is_reward: bool = False, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_reward_set(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        is_reward: bool = False, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开启或关闭打赏

        POST https://www.123pan.com/api/restful/goapi/v1/share/reward/status

        :payload:
            - ids: list[int | str] 💡 分享 id
            - isReward: 0 | 1 = 1
        """
        api = "restful/goapi/v1/share/reward/status"
        if isinstance(payload, (int, str)):
            payload = {"ids": [payload]}
        elif not isinstance(payload, dict):
            payload = {"ids": list(payload)}
        payload = dict_to_lower_merge(payload, is_reward=int(is_reward))
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def share_traffic_set(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_traffic_set(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_traffic_set(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """流量包设置

        PUT https://www.123pan.com/api/restful/goapi/v1/share/info

        :payload:
            - shareId: int | str
            - trafficLimit: int = <default>         💡 流量限制额度，单位字节
            - trafficLimitSwitch: 1 | 2 = <default> 💡 是否开启流量限制：1:关闭 2:开启
            - trafficSwitch: 1 | 2 = <default>      💡 是否开启免登录流量包：1:关闭 2:开启
            - ...
        """
        api = "restful/goapi/v1/share/info"
        return self.request(url=api, method="PUT", json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def upload_auth(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_auth(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_auth(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """认证上传信息，获取上传链接

        POST https://www.123pan.com/api/file/s3_upload_object/auth

        .. note::
            只能获取 1 个上传链接，用于非分块上传

        :payload:
            - bucket: str
            - key: str
            - storageNode: str
            - uploadId: str
        """
        api = "file/s3_upload_object/auth"
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def upload_complete(
        self, 
        payload: dict, 
        /, 
        is_multipart: bool = False, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_complete(
        self, 
        payload: dict, 
        /, 
        is_multipart: bool = False, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_complete(
        self, 
        payload: dict, 
        /, 
        is_multipart: bool = False, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """完成上传

        POST https://www.123pan.com/api/file/upload_complete/v2

        :payload:
            - FileId: int 💡 文件 id
            - bucket: str 💡 存储桶
            - key: str
            - storageNode: str
            - uploadId: str
            - isMultipart: bool = True 💡 是否分块上传
        """
        api = "file/upload_complete/v2"
        payload = dict_to_lower_merge(payload, isMultipart=is_multipart)
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def upload_prepare_parts(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_prepare_parts(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_prepare_parts(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """认证上传信息，获取上传链接

        POST https://www.123pan.com/api/file/s3_repare_upload_parts_batch

        .. note::
            一次可获取 `partNumberEnd - partNumberStart` 个上传链接，用于分块上传

        :payload:
            - bucket: str
            - key: str
            - storageNode: str
            - uploadId: str
            - partNumberStart: int = 1 💡 开始的分块编号（从 0 开始编号）
            - partNumberEnd: int = <default> 💡 结束的分块编号（不含）
        """
        api = "file/s3_repare_upload_parts_batch"
        if "partNumberStart" not in payload:
            payload["partNumberStart"] = 1
        if "partNumberEnd" not in payload:
            payload["partNumberEnd"] = int(payload["partNumberStart"]) + 1
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def upload_list_parts(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_list_parts(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_list_parts(
        self, 
        payload: dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """罗列已经上传的分块

        POST https://www.123pan.com/api/file/s3_list_upload_parts

        :payload:
            - bucket: str
            - key: str
            - storageNode: str
            - uploadId: str
        """
        api = "file/s3_list_upload_parts"
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    @overload
    def upload_request(
        self, 
        payload: str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_request(
        self, 
        payload: str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_request(
        self, 
        payload: str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """请求上传，获取一些初始化信息

        POST https://www.123pan.com/api/file/upload_request

        .. note::
            当响应信息里面有 "Reuse" 的值为 "true"，说明已经存在目录或者文件秒传

        :payload:
            - fileName: str 💡 文件或目录的名字
            - driveId: int | str = 0
            - duplicate: 0 | 1 | 2 = 0 💡 处理同名：0: 提示/忽略 1: 保留两者 2: 替换
            - etag: str = "" 💡 文件的 MD5 散列值
            - parentFileId: int | str = 0 💡 父目录 id
            - size: int = 0 💡 文件大小
            - type: 0 | 1 = 1 💡 类型，如果是目录则是 1，如果是文件则是 0
            - NotReuse: bool = False 💡 不要重用（仅在 `type=1` 时有效，如果为 False，当有重名时，立即返回，此时 `duplicate` 字段无效）
            - ...
        """
        api = "file/upload_request"
        if isinstance(payload, str):
            payload = {"fileName": payload}
        payload = dict_to_lower_merge(payload, {
            "driveId": 0, 
            "duplicate": 0, 
            "etag": "", 
            "parentFileId": 0,
            "size": 0, 
            "type": 1, 
            "NotReuse": False, 
        })
        if payload["size"] or payload["etag"]:
            payload["type"] = 0
        return self.request(url=api, json=payload, base_url=base_url, async_=async_, **request_kwargs)

    # TODO: 支持断点续传，也就是传入复传信息
    # TODO: 支持如果文件未曾打开，则可等尝试秒传失败之后，再行打开（因为如果能秒传，则根本不必打开）
    @overload
    def upload_file(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] ), 
        file_md5: str = "", 
        file_name: str = "", 
        file_size: int = -1, 
        parent_id: int = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        upload_data: None | dict = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_file(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer] ), 
        file_md5: str = "", 
        file_name: str = "", 
        file_size: int = -1, 
        parent_id: int = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        upload_data: None | dict = None, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_file(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer] ), 
        file_md5: str = "", 
        file_name: str = "", 
        file_size: int = -1, 
        parent_id: int = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        upload_data: None | dict = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """上传文件

        .. note::
            如果文件名中包含 Windows 文件名非法字符，则转换为对应的全角字符

        :param file: 待上传的文件

            - 如果为 `collections.abc.Buffer`，则作为二进制数据上传
            - 如果为 `filewrap.SupportsRead`，则作为可读的二进制文件上传
            - 如果为 `str` 或 `os.PathLike`，则视为路径，打开后作为文件上传
            - 如果为 `yarl.URL` 或 `http_request.SupportsGeturl` (`pip install python-http_request`)，则视为超链接，打开后作为文件上传
            - 如果为 `collections.abc.Iterable[collections.abc.Buffer]` 或 `collections.abc.AsyncIterable[collections.abc.Buffer]`，则迭代以获取二进制数据，逐步上传

        :param file_md5: 文件的 MD5 散列值
        :param file_name: 文件名
        :param file_size: 文件大小
        :param parent_id: 要上传的目标目录
        :param duplicate: 处理同名：0: 提示/忽略 1: 保留两者 2: 替换
        :param upload_data: 上传信息，用于断点续传，提供此参数，则会忽略 `file_md5`、`file_name`、`file_size`、`parent_id` 和 `duplicate`
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数

        :return: 接口响应
        """ 
        def gen_step():
            nonlocal file, file_md5, file_name, file_size
            def do_upload(file):
                return self.upload_file(
                    file=file, 
                    file_md5=file_md5, 
                    file_name=file_name, 
                    file_size=file_size, 
                    parent_id=parent_id, 
                    duplicate=duplicate, 
                    base_url=base_url, 
                    async_=async_, 
                    **request_kwargs, 
                )
            try:
                file = getattr(file, "getbuffer")()
            except (AttributeError, TypeError):
                pass
            if isinstance(file, Buffer):
                file_size = buffer_length(file)
                if not file_md5:
                    file_md5 = md5(file).hexdigest()
            elif isinstance(file, (str, PathLike)):
                path = fsdecode(file)
                if not file_name:
                    file_name = basename(path)
                if async_:
                    async def request():
                        async with async_open(path, "rb") as file:
                            setattr(file, "fileno", file.file.fileno)
                            setattr(file, "seekable", lambda: True)
                            return await do_upload(file)
                    return request
                else:
                    return do_upload(open(path, "rb"))
            elif isinstance(file, SupportsRead):
                seek = getattr(file, "seek", None)
                seekable = False
                curpos = 0
                if callable(seek):
                    if async_:
                        seek = ensure_async(seek, threaded=True)
                    try:
                        seekable = getattr(file, "seekable")()
                    except (AttributeError, TypeError):
                        try:
                            curpos = yield seek(0, 1)
                            seekable = True
                        except Exception:
                            seekable = False
                if not file_md5:
                    if not seekable:
                        fsrc = file
                        file = TemporaryFile()
                        if async_:
                            yield copyfileobj_async(fsrc, file)
                        else:
                            copyfileobj(fsrc, file)
                        file.seek(0)
                        return do_upload(file)
                    try:
                        if async_:
                            file_size, hashobj = yield file_digest_async(file)
                        else:
                            file_size, hashobj = file_digest(file)
                    finally:
                        yield seek(curpos)
                    file_md5 = hashobj.hexdigest()
                if file_size < 0:
                    try:
                        fileno = getattr(file, "fileno")()
                        file_size = fstat(fileno).st_size - curpos
                    except (AttributeError, TypeError, OSError):
                        try:
                            file_size = len(file) - curpos # type: ignore
                        except TypeError:
                            if seekable:
                                try:
                                    file_size = (yield seek(0, 2)) - curpos
                                finally:
                                    yield seek(curpos)
            elif isinstance(file, (URL, SupportsGeturl)):
                if isinstance(file, URL):
                    url = str(file)
                else:
                    url = file.geturl()
                if async_:
                    from httpfile import AsyncHttpxFileReader
                    async def request():
                        file = await AsyncHttpxFileReader.new(url)
                        async with file:
                            return await do_upload(file)
                    return request
                else:
                    from httpfile import HTTPFileReader
                    with HTTPFileReader(url) as file:
                        return do_upload(file)
            elif not file_md5 or file_size < 0:
                if async_:
                    file = bytes_iter_to_async_reader(file) # type: ignore
                else:
                    file = bytes_iter_to_reader(file) # type: ignore
                return do_upload(file)
            if not file_name:
                file_name = getattr(file, "name", "")
                file_name = basename(file_name)
            if file_name:
                file_name = file_name.translate(NAME_TANSTAB_FULLWIDH)
            else:
                file_name = str(uuid4())
            if file_size < 0:
                file_size = getattr(file, "length", 0)
            resp = yield self.upload_request(
                {
                    "etag": file_md5, 
                    "fileName": file_name, 
                    "size": file_size, 
                    "parentFileId": parent_id, 
                    "type": 0, 
                    "duplicate": duplicate, 
                }, 
                base_url=base_url, 
                async_=async_, 
                **request_kwargs, 
            )
            if resp.get("code", 0) not in (0, 200):
                return resp
            upload_data = resp["data"]
            if upload_data["Reuse"]:
                return resp
            slice_size = int(upload_data["SliceSize"])
            upload_request_kwargs = {
                **request_kwargs, 
                "method": "PUT", 
                "headers": {"authorization": ""}, 
                "parse": ..., 
            }
            if file_size > slice_size:
                upload_data["partNumberStart"] = 1
                q, r = divmod(file_size, slice_size)
                upload_data["partNumberEnd"] = q + 1 + (r > 0)
                resp = yield self.upload_prepare_parts(
                    upload_data, 
                    base_url=base_url, 
                    async_=async_, 
                    **request_kwargs, 
                )
                check_response(resp)
                d_urls = resp["data"]["presignedUrls"]
                urls = (d_urls[str(i)] for i in range(1, len(d_urls) + 1))
                if async_:
                    async def request():
                        chunks = bio_chunk_async_iter(file, chunksize=slice_size) # type: ignore
                        async for chunk in chunks:
                            await self.request(next(urls), data=chunk, async_=True, **upload_request_kwargs)
                    yield request
                else:
                    chunks = bio_chunk_iter(file, chunksize=slice_size) # type: ignore
                    for chunk, url in zip(chunks, urls):
                        self.request(url, data=chunk, **upload_request_kwargs)
            else:
                resp = yield self.upload_auth(
                    upload_data, 
                    base_url=base_url, 
                    async_=async_, 
                    **request_kwargs, 
                )
                check_response(resp)
                url = resp["data"]["presignedUrls"]["1"]
                yield self.request(url, data=file, async_=async_, **upload_request_kwargs)
            upload_data["isMultipart"] = file_size > slice_size
            return self.upload_complete(
                upload_data, 
                base_url=base_url, 
                async_=async_, 
                **request_kwargs, 
            )
        return run_gen_step(gen_step, async_=async_)

    @overload
    def upload_file_fast(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] ) = b"", 
        file_md5: str = "", 
        file_name: str = "", 
        file_size: int = -1, 
        parent_id: int = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_file_fast(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer] ) = b"", 
        file_md5: str = "", 
        file_name: str = "", 
        file_size: int = -1, 
        parent_id: int = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_file_fast(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer] ) = b"", 
        file_md5: str = "", 
        file_name: str = "", 
        file_size: int = -1, 
        parent_id: int = 0, 
        duplicate: Literal[0, 1, 2] = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """尝试秒传文件，如果失败也直接返回

        :param file: 待上传的文件

            - 如果为 `collections.abc.Buffer`，则作为二进制数据上传
            - 如果为 `filewrap.SupportsRead`，则作为可读的二进制文件上传
            - 如果为 `str` 或 `os.PathLike`，则视为路径，打开后作为文件上传
            - 如果为 `yarl.URL` 或 `http_request.SupportsGeturl` (`pip install python-http_request`)，则视为超链接，打开后作为文件上传
            - 如果为 `collections.abc.Iterable[collections.abc.Buffer]` 或 `collections.abc.AsyncIterable[collections.abc.Buffer]`，则迭代以获取二进制数据，逐步上传

        :param file_md5: 文件的 MD5 散列值
        :param file_name: 文件名
        :param file_size: 文件大小
        :param parent_id: 要上传的目标目录
        :param duplicate: 处理同名：0: 提示/忽略 1: 保留两者 2: 替换
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数

        :return: 接口响应
        """ 
        def gen_step():
            nonlocal file, file_md5, file_name, file_size
            if file_md5 and file_size >= 0:
                pass
            elif file:
                def do_upload(file):
                    return self.upload_file_fast(
                        file=file, 
                        file_md5=file_md5, 
                        file_name=file_name, 
                        file_size=file_size, 
                        parent_id=parent_id, 
                        duplicate=duplicate, 
                        base_url=base_url, 
                        async_=async_, 
                        **request_kwargs, 
                    )
                try:
                    file = getattr(file, "getbuffer")()
                except (AttributeError, TypeError):
                    pass
                if isinstance(file, Buffer):
                    file_size = buffer_length(file)
                    if not file_md5:
                        file_md5 = md5(file).hexdigest()
                elif isinstance(file, (str, PathLike)):
                    path = fsdecode(file)
                    if not file_name:
                        file_name = basename(path)
                    if async_:
                        async def request():
                            async with async_open(path, "rb") as file:
                                return await do_upload(file)
                        return request
                    else:
                        return do_upload(open(path, "rb"))
                elif isinstance(file, SupportsRead):
                    if not file_md5 or file_size < 0:
                        if async_:
                            file_size, hashobj = yield file_digest_async(file)
                        else:
                            file_size, hashobj = file_digest(file)
                        file_md5 = hashobj.hexdigest()
                elif isinstance(file, (URL, SupportsGeturl)):
                    if isinstance(file, URL):
                        url = str(file)
                    else:
                        url = file.geturl()
                    if async_:
                        from httpfile import AsyncHttpxFileReader
                        async def request():
                            file = await AsyncHttpxFileReader.new(url)
                            async with file:
                                return await do_upload(file)
                        return request
                    else:
                        from httpfile import HTTPFileReader
                        with HTTPFileReader(url) as file:
                            return do_upload(file)
                elif not file_md5 or file_size < 0:
                    if async_:
                        file = bytes_iter_to_async_reader(file) # type: ignore
                    else:
                        file = bytes_iter_to_reader(file) # type: ignore
                    return do_upload(file)
            else:
                file_md5 = "d41d8cd98f00b204e9800998ecf8427e"
                file_size = 0
            if not file_name:
                file_name = getattr(file, "name", "")
                file_name = basename(file_name)
            if file_name:
                file_name = file_name.translate(NAME_TANSTAB_FULLWIDH)
            if not file_name:
                file_name = str(uuid4())
            if file_size < 0:
                file_size = getattr(file, "length", 0)
            return self.upload_request(
                {
                    "etag": file_md5, 
                    "fileName": file_name, 
                    "size": file_size, 
                    "parentFileId": parent_id, 
                    "type": 0, 
                    "duplicate": duplicate, 
                }, 
                base_url=base_url, 
                async_=async_, 
                **request_kwargs, 
            )
        return run_gen_step(gen_step, async_=async_)

    @overload
    def user_info(
        self, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_info(
        self, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_info(
        self, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """用户信息

        GET https://www.123pan.com/api/user/info
        """
        api = "user/info"
        return self.request(url=api, method="GET", base_url=base_url, async_=async_, **request_kwargs)

    @overload
    @staticmethod
    def user_login(
        payload: dict, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def user_login(
        payload: dict, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def user_login(
        payload: dict, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """使用账号和密码登录

        POST https://www.123pan.com/api/user/sign_in

        .. note::
            获取的 token 有效期 30 天

        :payload:
            - passport: int | str   💡 手机号或邮箱
            - password: str         💡 密码
            - remember: bool = True 💡 是否记住密码（不用管）
        """
        api = f"{base_url or DEFAULT_LOGIN_BASE_URL}/api/user/sign_in"
        request_kwargs.setdefault("parse", default_parse)
        if request is None:
            return get_default_request()(url=api, method="POST", json=payload, async_=async_, **request_kwargs)
        else:
            return request(url=api, method="POST", json=payload, **request_kwargs)

    @overload
    @staticmethod
    def open_access_token(
        payload: dict, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def open_access_token(
        payload: dict, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def open_access_token(
        payload: dict, 
        /, 
        request: None | Callable = None, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：获取 access_token

        POST https://open-api.123pan.com/api/v1/access_token

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/sg2gvfk5i3dwoxtg

        :payload:
            - clientID: str
            - clientSecret: str
        """
        api = f"{base_url or DEFAULT_OPEN_BASE_URL}/api/v1/access_token"
        request_kwargs.setdefault("parse", default_parse)
        if request is None:
            return get_default_request()(url=api, method="POST", json=payload, async_=async_, **request_kwargs)
        else:
            return request(url=api, method="POST", json=payload, **request_kwargs)

    @overload
    def open_download_url(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_download_url(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_download_url(
        self, 
        payload: int | str | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：获取下载直链

        GET https://open-api.123pan.com/api/v1/direct-link/url

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/tdxfsmtemp4gu4o2

        .. note::
            需要开通会员

        :payload:
            - fileID: int | str 💡 文件 id
        """
        api = "v1/direct-link/url"
        if isinstance(payload, (int, str)):
            payload = {"fileID": payload}
        return self.request(url=api, method="GET", params=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_fs_delete(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_delete(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_delete(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：彻底删除

        POST https://open-api.123pan.com/api/v1/file/delete

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/sg2gvfk5i3dwoxtg

        :payload:
            - fileIDs: list[int | str] 💡 文件 id 数组，长度最大不超过 100
        """
        api = "v1/file/delete"
        if isinstance(payload, (int, str)):
            payload = {"fileIDs": [payload]}
        elif not isinstance(payload, dict):
            if not isinstance(payload, (tuple, list)):
                payload = list(payload)
            payload = {"fileIDs": payload}
        return self.request(url=api, json=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_fs_info(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_info(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_info(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：获取文件信息

        GET https://open-api.123pan.com/api/v1/file/detail

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/uxomcu64kefnbdvz

        :payload:
            - fileID: int | str
        """
        api = "v1/file/detail"
        if isinstance(payload, (int, str)):
            payload = {"fileID": payload}
        return self.request(url=api, method="GET", params=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_fs_list_v1(
        self, 
        payload: int | str | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_list_v1(
        self, 
        payload: int | str | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_list_v1(
        self, 
        payload: int | str | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：获取文件列表（可搜索）

        GET https://open-api.123pan.com/api/v1/file/list

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/am42fselaozmg123

        .. note::
            如果返回信息中，有 "Next" 的值为 "-1"，说明无下一页

        :payload:
            - limit: int = 100 💡 分页大小，最大不超过100
            - orderBy: str = "file_id" 💡 排序依据："file_id", "file_name", "create_at", "update_at", "size", "share_id", ...
            - orderDirection: "asc" | "desc" = "asc" 💡 排序顺序
            - page: int = 1 💡 第几页，从 1 开始，可以是 0
            - parentFileId: int | str = 0 💡 父目录 id
            - trashed: "false" | "true" = <default> 💡 是否查看回收站的文件
            - searchData: str = <default> 💡 搜索关键字（将无视 `parentFileId` 参数）
        """
        api = "v1/file/list"
        if isinstance(payload, (int, str)):
            payload = {"parentFileId": payload}
        payload = dict_to_lower_merge(payload, {
            "limit": 100, 
            "orderBy": "file_id", 
            "orderDirection": "desc", 
            "page": 1, 
            "parentFileId": 0, 
        })
        return self.request(url=api, method="GET", params=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_fs_list_v2(
        self, 
        payload: int | str | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_list_v2(
        self, 
        payload: int | str | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_list_v2(
        self, 
        payload: int | str | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：获取文件列表（可搜索）

        GET https://open-api.123pan.com/api/v2/file/list

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/rei7kh5mnze2ad4q

        .. note::
            如果返回信息中，有 "Next" 的值为 "-1"，说明无下一页

        :payload:
            - lastFileId: int = <default> 💡 上一页的最后一条记录的 FileID，翻页查询时需要填写
            - limit: int = 100 💡 分页大小，最大不超过100
            - parentFileId: int | str = 0 💡 父目录 id
            - SearchData: str = <default> 💡 搜索关键字（将无视 `parentFileId` 参数）
            - searchMode: 0 | 1 = 0 💡 搜索模式

                .. note::
                    - 0: 全文模糊搜索（将会根据搜索项分词,查找出相似的匹配项）
                    - 1: 精准搜索（精准搜索需要提供完整的文件名）
        """
        api = "v2/file/list"
        if isinstance(payload, (int, str)):
            payload = {"parentFileId": payload}
        payload = dict_to_lower_merge(payload, {
            "limit": 100, 
            "parentFileId": 0, 
            "searchMode": 0, 
        })
        return self.request(url=api, method="GET", params=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    open_fs_list = open_fs_list_v2

    @overload
    def open_fs_mkdir(
        self, 
        payload: str | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_mkdir(
        self, 
        payload: str | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_mkdir(
        self, 
        payload: str | dict, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：创建目录

        POST https://open-api.123pan.com/upload/v1/file/mkdir

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/gvz09ibuuo97i5ue

        :payload:
            - name: str
            - parentID: int | str = 0
        """
        api = "/upload/v1/file/mkdir"
        if isinstance(payload, str):
            payload = {"name": payload}
        payload = dict_to_lower_merge(payload, parentID=parent_id)
        return self.request(url=api, json=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_fs_move(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_move(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_move(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        parent_id: int | str = 0, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：从回收站恢复文件

        POST https://open-api.123pan.com/api/v1/file/move

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/kx9f8b6wk6g55uwy

        :payload:
            - fileIDs: list[int | str] 💡 文件 id 数组，长度最大不超过 100
            - toParentFileID: int | str = 0
        """
        api = "v1/file/move"
        if isinstance(payload, (int, str)):
            payload = {"fileIDs": [payload]}
        elif not isinstance(payload, dict):
            if not isinstance(payload, (tuple, list)):
                payload = list(payload)
            payload = {"fileIDs": payload}
        payload = dict_to_lower_merge(payload, toParentFileID=parent_id)
        return self.request(url=api, json=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_fs_rename(
        self, 
        payload: str | Iterable[str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_rename(
        self, 
        payload: str | Iterable[str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_rename(
        self, 
        payload: str | Iterable[str] | dict, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：重命名

        POST https://open-api.123pan.com/api/v1/file/rename

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/ec18ovepgciazfuc

        :payload:
            - renameList: list[str] 💡 数组，最多 30 个成员，每个成员的格式为 "文件ID|新的文件名"
        """
        api = "v1/file/rename"
        if isinstance(payload, str):
            payload = {"renameList": [payload]}
        elif not isinstance(payload, dict):
            if not isinstance(payload, (tuple, list)):
                payload = list(payload)
            payload = {"renameList": payload}
        return self.request(url=api, json=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_fs_trash(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_trash(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_trash(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：删除文件，放入回收站中

        POST https://open-api.123pan.com/api/v1/file/trash

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/en07662k2kki4bo6

        :payload:
            - fileIDs: list[int | str] 💡 文件 id 数组，长度最大不超过 100
        """
        api = "v1/file/trash"
        if isinstance(payload, (int, str)):
            payload = {"fileIDs": [payload]}
        elif not isinstance(payload, dict):
            if not isinstance(payload, (tuple, list)):
                payload = list(payload)
            payload = {"fileIDs": payload}
        return self.request(url=api, json=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_fs_trash_recover(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_fs_trash_recover(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_fs_trash_recover(
        self, 
        payload: int | str | Iterable[int | str] | dict = 0, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：从回收站恢复文件

        POST https://open-api.123pan.com/api/v1/file/recover

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/kx9f8b6wk6g55uwy

        :payload:
            - fileIDs: list[int | str] 💡 文件 id 数组，长度最大不超过 100
        """
        api = "v1/file/recover"
        if isinstance(payload, (int, str)):
            payload = {"fileIDs": [payload]}
        elif not isinstance(payload, dict):
            if not isinstance(payload, (tuple, list)):
                payload = list(payload)
            payload = {"fileIDs": payload}
        return self.request(url=api, json=payload, base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

    @overload
    def open_user_info(
        self, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def open_user_info(
        self, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def open_user_info(
        self, 
        /, 
        base_url: str = "", 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开放接口：用户信息

        GET https://open-api.123pan.com/api/v1/user/info

        .. tip::
            https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/fa2w0rosunui2v4m
        """
        api = "v1/user/info"
        return self.request(url=api, method="GET", base_url=(base_url or DEFAULT_OPEN_BASE_URL), async_=async_, **request_kwargs)

# TODO: 再添加一组开放接口，文档：https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced

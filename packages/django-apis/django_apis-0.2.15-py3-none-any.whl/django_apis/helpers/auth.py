import base64
from django_apis.exceptions import Forbidden
from jsonpath_ng.ext import parse as json_parser
from .base import ApiviewHelperBase
from ..settings import DJANGO_APIS_APIKEYS
from ..settings import DJANGO_APIS_USERS

__all__ = [
    "HttpApiKeyStorageBase",
    "HttpBasicAuthUserStorageBase",
    "SimpleHttpApiKeyStorage",
    "SimpleHttpBasicAuthUserStorage",
    "http_bearer_auth_protect",
    "http_basic_auth_protect",
    "apikey_auth_protect",
]

class HttpApiKeyStorageBase(object):
    def authenticate(self, apikey):
        raise NotImplementedError()


class HttpBasicAuthUserStorageBase(object):
    def authenticate(self, username, password):
        raise NotImplementedError()

class SimpleHttpApiKeyStorage(HttpApiKeyStorageBase):
    def __init__(self, apikeys):
        self.apikeys = apikeys

    def authenticate(self, apikey):
        return (apikey in self.apikeys)

class SimpleHttpBasicAuthUserStorage(HttpBasicAuthUserStorageBase):
    def __init__(self, users):
        self.users = users
    
    def authenticate(self, username, password):
        if not username in self.users:
            return False
        if password != self.users[username]:
            return False
        return True




class http_bearer_auth_protect(ApiviewHelperBase):
    """HTTP BEARER认证。

    客户端在请求头不添加：
        Authorization: Bearer xxx
    """
    def __init__(self, apikey_storage=None, header="Authorization"):
        self.apikey_storage = apikey_storage or SimpleHttpApiKeyStorage(DJANGO_APIS_APIKEYS)
        self.header = header

    def get_response(self, view, request, **kwargs):
        # 从请求中提取apikey
        authorization = request.META.get("HTTP_" + self.header.upper(), None)
        if not authorization:
            raise Forbidden()
        # apikey格式处理
        if authorization.startswith("Bearer "):
            authorization = authorization[7:].strip()
        # 判断是否为信任apikey
        if not apikey_storage.authenticate(authorization):
            raise Forbidden()
        # 继续处理请求
        return super().get_response(view, request, **kwargs)



class http_basic_auth_protect(ApiviewHelperBase):
    """Http Basic请求头认证"""

    def __init__(self, user_storage:SimpleHttpBasicAuthUserStorage=None, header="Authorization"):
        self.header = header
        self.user_storage = users or SimpleHttpBasicAuthUserStorage(DJANGO_APIS_USERS)
    
    def get_response(self, view, request, **kwargs):
        """Http Basic请求头认证"""
        # 从请求中提取username&password组合
        authorization = request.META.get("HTTP_" + header.upper(), None)
        if not authorization:
            raise Forbidden()
        if len(authorization) % 4:
            authorization += "=" * ((4 - len(authorization) % 4) % 4)
        authorization = base64.decodebytes(authorization.encode()).decode()
        if not ":" in authorization:
            raise Forbidden()
        username_input, password_input = authorization.split(":", 1)
        # 判断是否为信任username&password组合
        if not self.user_storage.authenticate(username=username_input, password=password_input):
            raise Forbidden()
        # 继续处理请求
        return super().get_response(view, request, **kwargs)


def apikey_auth_protect(
    request,
    apikeys,
    headers="apikey",
    query_fields=None,
    payload_fields=None,
    form_fields=None,
    cookie_fields=None,
):
    """开放式的apikey认证"""
    if isinstance(headers, str):
        headers = [headers]
    apikey_input = None
    if not apikey_input and headers:
        for header in headers:
            apikey_input = request.META.get("HTTP_" + header.upper(), None)
            if apikey_input:
                break
    if not apikey_input and cookie_fields:
        for field in cookie_fields:
            apikey_input = request.COOKIES.get(field, None)
            if apikey_input:
                break
    if not apikey_input and form_fields:
        for field in form_fields:
            apikey_input = request.POST.get(field, None)
            if apikey_input:
                break
    if not apikey_input and payload_fields:
        try:
            payload = json.loads(request.body)
        except:
            payload = {}
        for field in payload_fields:
            if field.startswith("$") or ("." in field):
                parser = json_parser(field)
                for item in parser.find(payload):
                    apikey_input = item.value
                    if apikey_input:
                        break
            else:
                apikey_input = payload.get(field, None)
                if apikey_input:
                    break
    if not apikey_input and query_fields:
        for field in query_fields:
            apikey_input = request.GET.get(field, None)
            if apikey_input:
                break
    if not apikey_input:
        raise Forbidden()
    if apikey_input.startswith("Bearer "):
        apikey_input = apikey_input[7:]
    elif apikey_input.startswith("Basic "):
        apikey_input = apikey_input[6:]
    if not apikey_input in apikeys:
        raise Forbidden()
    return apikey_input

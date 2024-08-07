import json

from werkzeug.exceptions import HTTPException
from typing_extensions import override


class APIException(HTTPException):
    """
    定义自定义异常类，基类继承自HTTPException
    """

    def __init__(self, code=None,  msg=None, error_code=None, data=None):
        """
        自定义异常构造函数
        :param msg: 接口返回信息
        :param error_code: 接口返回自定义错误码
        :param data: 接口返回数据
        """
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if data:
            self.data = data

        super(APIException, self).__init__(msg, None)

    @override
    def get_body(self, environ=None, scope=None):
        """
        获取异常信息，并以json格式返回
        :return:
        """
        res = {"code": self.code, "data": self.data, "msg": self.msg, "error_code": self.error_code}
        try:
            res_body_json = json.dumps(res)
        except Exception as e:
            raise e
        return res_body_json

    @override
    def get_headers(self, environ=None, scope=None):
        return [('Content-Type', 'application/json; charset=utf-8')]


class HttpOk(APIException):
    code = 200
    msg = "Ok"
    error_code = 0
    data = None


class ClientParameterFailed(APIException):
    code = 400
    msg = "Bad Request, Please Check You Input Body"
    error_code = 10001
    data = None


class ClientAuthFailed(APIException):
    code = 401
    msg = "Unauthorized"
    error_code = 10002
    data = None


class ClientPermissionFailed(APIException):
    code = 403
    msg = "Forbidden, Please make sure you have the right permission"
    error_code = 10003
    data = None


class ClientResourceNotFoundFail(APIException):
    code = 404
    msg = "Resource Not Found"
    error_code = 10005
    data = None


class ServerErrorInternalServerError(APIException):
    code = 500
    msg = "Internal Server Error"
    error_code = 200001
    data = None


class ServerErrorBadGateway(APIException):
    code = 502
    msg = "Bad Gateway"
    error_code = 200002
    data = None


class ServerErrorServiceUnavailable(APIException):
    code = 503
    msg = "Service Unavailable"
    error_code = 200003
    data = None


class ServerErrorGatewayTimeout(APIException):
    code = 504
    msg = "Gateway Timeout"
    error_code = 200004
    data = None






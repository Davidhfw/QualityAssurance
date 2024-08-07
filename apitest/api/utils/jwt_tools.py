from flask import Flask, request, jsonify
import jwt
import datetime

from apitest.api.api_exceptions import ClientAuthFailed

# 用于签名的密钥
SECRET_KEY = 'your_secret_key'

def create_jwt(payload):
    """
    创建一个JWT。

    参数:
    payload (dict): 要包含在JWT中的数据。

    返回:
    str: 生成的JWT。
    """
    # 设置JWT的过期时间
    expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    payload['exp'] = expiration_time

    # 生成JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt(token):
    """
    验证JWT的有效性。

    参数:
    token (str): 要验证的JWT。

    返回:
    dict or None: 如果验证成功，返回payload；否则返回None。
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login(user_name, pwd):
    # 这里应该是用户登录的逻辑，为了示例简单，我们直接创建一个JWT
    payload = {'username': user_name, 'pwd': pwd}
    return create_jwt(payload)


def secure(auth):
    # 从请求头中获取JWT
    # auth_header = request.headers.get('Authorization')
    auth_header = auth
    token = ""
    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        raise ClientAuthFailed(msg='Token is missing')

    # 验证JWT
    payload = verify_jwt(token)
    if payload is None:
        raise ClientAuthFailed(msg='Invalid Token')

    # 如果验证成功，返回安全数据
    return token


if __name__ == '__main__':
    token = login("root", "123456")
    auth = f"Authorization: {token}"
    print(secure(auth))

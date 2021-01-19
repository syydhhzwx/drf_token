import jwt
from rest_framework import exceptions
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler


class MyAuthentication(BaseJSONWebTokenAuthentication):

    def authenticate(self, request):
        # 获取到前端传递的token
        jwt_token = request.META.get("HTTP_AUTHORIZATION")

        # 自定义token的校验规则
        token = self.parse_jwt_token(jwt_token)

        if token is None:
            return None

        # 如果token不为空 将token反解析出载荷
        try:
            # 通过前端传递的token解析出载荷
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed("签名已过期，请重新登录")
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('非法请求，伪造的签名')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        # 如果载荷解析没问题，则返回用户
        user = self.authenticate_credentials(payload)

        return user, token

    def parse_jwt_token(self, token):
        tokens = token.split()

        # 三段式
        if len(tokens) != 3 or tokens[0].lower() != "auth" or tokens[2].lower() != "jwt":
            return None

        return tokens[1]

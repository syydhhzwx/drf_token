import re

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from api.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserModelSerializer(ModelSerializer):
    # 自定义反序列化字段  代表这个字段只参与反序列化 且不会要求与模型中的字段进行匹配
    account = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["account", "pwd", "username", "phone", "email"]

        # 指定的是模型的字段
        extra_kwargs = {
            "username": {
                "read_only": True
            },
            "phone": {
                "read_only": True
            },
            "email": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        # 根据前端的参数得到合法用户
        account = attrs.get("account")
        pwd = attrs.get("pwd")

        # 根据各种登录条件完成登录  用户名  邮箱  手机号
        if re.match(r'.+@.+', account):
            # 代表输入的邮箱
            user_obj = User.objects.filter(email=account).first()
        elif re.match(r'1[3-9][0-9]{9}', account):
            # 代表输入的是手机号
            user_obj = User.objects.filter(phone=account).first()
        else:
            # 代表输入的是用户名
            user_obj = User.objects.filter(username=account).first()

        # 判断用户是否存在 且用户的密码是否正确
        # check_password: 校验密码是否正确
        # make_password: 对明文密码进行加密
        if user_obj and user_obj.check_password(pwd):
            # 签发token
            # TODO 根据合法用户生成载荷  根据载荷生成token
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            self.obj = user_obj
            self.token = token
        else:
            raise serializers.ValidationError("未得到合法用户")

        return attrs

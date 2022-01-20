from typing import Dict

from flask_marshmallow.sqla import SQLAlchemyAutoSchema, auto_field
from marshmallow import Schema, fields, validate, validates, ValidationError, decorators

from application import message, mysqldb, redis_check as redis
from .models import User


class MobileSchema(Schema):
    """手机号码验证"""
    mobile: fields.String = fields.String(required=True, validate=validate.Regexp(regex=r'^1[3-9]\d{9}$'),
                                          error=message.MOBILE_FORMAT_ERROR)

    @validates('mobile')
    def validate_mobile(self, mobile: str) -> str:
        if User.query.filter(User.mobile == mobile).first():
            raise ValidationError(message=message.MOBILE_EXISTS, field_name='mobile')
        return mobile


class UserSchema(SQLAlchemyAutoSchema):
    mobile = auto_field(required=True, load_only=True, validates=validate.Regexp(
        regex=r'^1[3-9]\d{9}$',
        error=message.MOBILE_FORMAT_ERROR
    ))
    password = fields.String(required=True, load_only=True, validate=validate.Length(
        min=6, max=16, error=message.PASSWORD_FORMAT_ERROR))
    password2 = fields.String(required=True, load_only=True)
    sms_code = fields.String(required=True, load_only=True, validate=validate.Length(
        min=4, max=4, error=message.SMS_CODE_FORMAT_ERROR))

    class Meta:
        model = User
        include_fk = True  # 启用外键关系
        include_relationships = True  # 模型关系外部属性
        # 如果要全换全部字段，就不要声明fields或exclude字段即可
        fields = ["id", "name", "mobile", "password", "password2", "sms_code"]
        sqla_session = mysqldb.session

    @decorators.validates_schema
    def validate(self, data, **kwargs) -> Dict[str, str]:
        # 校验密码和确认密码
        if data["password"] != data["password2"]:
            raise ValidationError(message=message.PASSWORD_NOT_MATCH, field_name="password")

        # 校验短信验证码
        # 1、redis中获取短信验证码
        redis_sms_code = redis.get(f"sms_{data['mobile']}")
        if redis_sms_code is None:
            raise ValidationError(message=message.SMS_CODE_EXPIRED, field_name="sms_code")
        redis_sms_code = redis_sms_code.decode()

        # 2、提取客户端的短信验证码
        sms_code = data['sms_code']

        # 3、删除redis中的验证码[减少暴力破解的风险]
        redis.delete("sms_%s" % data["mobile"])

        # 4. 字符串比较，如果失败，则抛出异常，否则，直接删除验证码
        if sms_code != redis_sms_code:
            raise ValidationError(message=message.SMS_CODE_NOT_MATCH, field_name="sms_code")
        data.pop("password2")
        data.pop("sms_code")
        return data

    @decorators.post_load
    def save_object(self, data, **kwargs) -> User:
        data["name"] = data["mobile"]
        user = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

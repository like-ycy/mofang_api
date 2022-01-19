from marshmallow import Schema, fields, validate, validates, ValidationError

from application import message
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

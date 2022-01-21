import random
from typing import Dict, Union, Any

from application import message, code
from application import redis_check as redis
from .serializers import MobileSchema, ValidationError, UserSchema
from .tasks import send_sms


def check_mobile(mobile: str) -> Dict[str, Union[str, int]]:
    """
    验证手机号码是否已经注册
    :param mobile: 手机号码
    :return: 一个字典，包含错误码和错误信息
    """
    mobile_schema = MobileSchema()
    try:
        mobile_schema.load({'mobile': mobile})
        result = {'errno': code.CODE_OK, 'errmsg': message.OK}
    except ValidationError as err:
        result = {'errno': code.CODE_VALIDATE_ERROR, 'errmsg': err.messages['mobile'][0]}

    return result


def register(mobile: str, password: str, password2: str, sms_code: str) -> Dict[str, Any]:
    """
    注册
    :param mobile: 手机号
    :param password: 密码
    :param password2: 确认密码
    :param sms_code:  短信验证码
    :return:  一个字典，包含错误码和错误信息
    """
    try:
        ms = MobileSchema()
        ms.load({'mobile': mobile})
        us = UserSchema()
        user = us.load({'mobile': mobile, 'password': password, 'password2': password2, 'sms_code': sms_code})
        result = {"errno": code.CODE_OK, "errmsg": us.dump(user)}
    except ValidationError as e:
        result = {"errno": code.CODE_VALIDATE_ERROR, "errmsg": e.messages}
    return result


def sms(mobile: str) -> Dict[str, Any]:
    """
    发送短信验证码
    :param mobile: 手机号
    :return:
    """
    # 验证手机号码是否已经注册
    ret: Dict[str, Any] = check_mobile(mobile)
    if ret['errno'] != 0:
        return ret

    # 短信发送冷却时间
    time: int = redis.ttl(f'int_{mobile}')
    if time > 0:
        return {
            "errno": code.CODE_INTERVAL_TIME,
            "errmsg": message.SMS_INTERVAL_TIME,
            "data": {
                "time": time,
            }
        }
    # 生成短信验证码
    sms_code: str = "%04d" % random.randint(0, 9999)

    # 异步发送短信
    send_sms.delay(mobile=mobile, sms_code=sms_code)

    return {"errno": code.CODE_OK, "errmsg": message.OK}

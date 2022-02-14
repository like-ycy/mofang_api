import random
from typing import Dict, Union, Any

from application import message, code, get_user_object
from application import redis_check as redis
from flask_jwt_extended import get_jwt_identity, jwt_required
from .models import User
from .serializers import MobileSchema, ValidationError, UserSchema
from .services import gen_token, get_user_by_id, del_token, save_avatar, update_user
from .tasks import send_sms


def check_mobile(mobile: str) -> Dict[str, Union[str, int]]:
    """
    验证手机号码是否已经注册
    :param mobile: 手机号码
    :return: 一个字典，包含错误码和错误信息
    """
    mobile_schema = MobileSchema()
    try:
        mobile_schema.load({"mobile": mobile})
        result = {"errno": code.CODE_OK, "errmsg": message.OK}
    except ValidationError as err:
        result = {
            "errno": code.CODE_VALIDATE_ERROR,
            "errmsg": err.messages["mobile"][0],
        }

    return result


def register(
        mobile: str, password: str, password2: str, sms_code: str
) -> Dict[str, Any]:
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
        ms.load({"mobile": mobile})
        us = UserSchema()
        user = us.load(
            {
                "mobile": mobile,
                "password": password,
                "password2": password2,
                "sms_code": sms_code,
            }
        )
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
    if ret["errno"] != 0:
        return ret

    # 短信发送冷却时间
    time: int = redis.ttl(f"int_{mobile}")
    if time > 0:
        return {
            "errno": code.CODE_INTERVAL_TIME,
            "errmsg": message.SMS_INTERVAL_TIME,
            "data": {
                "time": time,
            },
        }
    # 生成短信验证码
    sms_code: str = "%04d" % random.randint(0, 9999)

    # 异步发送短信
    send_sms.delay(mobile=mobile, sms_code=sms_code)

    return {"errno": code.CODE_OK, "errmsg": message.OK}


def login(account: str, password: str) -> Dict[str, Any]:
    """
    用户jwt登录
    :param account: 账户名[可以是手机号、邮箱、用户名]
    :param password: 登录密码
    :return
    """
    # 验证数据
    try:
        us = UserSchema()
        user = us.load({"account": account, "password": password})
        palyload = us.dump(user)
        access_token, refresh_token = gen_token(palyload)
        result = {
            "errno": code.CODE_OK,
            "errmsg": message.OK,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        }
    except ValidationError as e:
        result = {"errno": code.CODE_VALIDATE_ERROR, "errmsg": e.messages}
    return result


@get_user_object  # 验证 jwt的 assess token
def info(user: User) -> Any:
    """获取用户身份信息"""
    user_info: Dict[str, Any] = get_jwt_identity()  # 获取refresh token中的载荷
    user_info['mobile'] = user.mobile
    return {"errno": code.CODE_OK, "errmsg": message.OK, "data": user_info}


@get_user_object
def verify(user: User) -> Any:
    """验证客户端上传的token，进行校验，以方便客户端判断用户的登录状态"""
    payload: Dict[str, Any] = get_jwt_identity()  # 获取refresh token中的载荷
    access_token, _ = gen_token(payload=payload)
    return {"errno": code.CODE_OK, "errmsg": message.OK, "access_token": access_token}


@jwt_required(refresh=True)  # 验证 jwt的 refresh token
def refresh() -> Dict[str, Any]:
    """刷新用户身份信息"""
    user_info: Dict[str, Any] = get_jwt_identity()  # 获取refresh token中的载荷
    user = get_user_by_id(user_info["id"])  # 根据id获取用户模型对象
    if user is None:
        return {"errno": code.CODE_USER_NOT_EXISTS, "errmsg": message.USER_NOT_EXISTS}

    # 生成新的access_token
    access_token, _ = gen_token(user_info)
    return {
        "errno": code.CODE_OK,
        "errmsg": message.OK,
        "data": {
            "access_token": access_token,
        },
    }


@jwt_required()
def logout() -> Any:
    """退出登录状态"""
    payload: Dict[str, Any] = get_jwt_identity()  # 获取refresh_token中的载荷
    # 删除redis中的access_token
    del_token(payload['id'])
    return {
        "errno": code.CODE_OK,
        "errmsg": message.OK
    }


@get_user_object
def avatar(user: User, img: str) -> Dict[str, Any]:
    """更新用户头像"""
    # 1、从base64内容中截取客户端上传头像图片格式
    ext = img[img.find('/') + 1:img.find(';')]
    # 2、判断格式是否符合要求
    if ext not in ["png", "svg", "jpeg", "jpg"]:
        return {
            "errno": code.CODE_IMAGE_FORMAT_ERROR,
            "errmsg": message.IMAGE_FORMAT_ERROR,
        }
    # 3、保存头像
    url = save_avatar(img, ext)
    # 4、更新用户信息，返回新的token
    user_info: Dict[str, Any] = get_jwt_identity()  # 获取refresh_token中的载荷
    update_user(user, {"avatar": url})
    user_info['avatar'] = url
    access_token, refresh_token = gen_token(user_info)  # 生成新的token
    return {
        "errno": code.CODE_OK,
        "errmsg": message.OK,
        "access_token": access_token,
        "refresh": refresh_token
    }

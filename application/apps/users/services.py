import base64
import uuid
from typing import Dict, Any, Tuple

from flask import current_app

from application import redis_cache as cache, mysqldb, oss
from flask_jwt_extended import create_access_token, create_refresh_token
from .models import User


def gen_token(payload: Dict[str, Any]) -> Tuple:
    """生成access_token和refresh_token"""
    access_token: str = create_access_token(identity=payload)  # identity 就是载荷
    refresh_token: str = create_refresh_token(identity=payload)
    # 缓存一个token到redis中，表示当前用户在服务端的登录状态，将来如果token或者删除数据库中用户信息时，会删除调用当前redis中保存的token
    cache.setex(
        f"access_token_{payload['id']}",
        current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        access_token,
    )

    return access_token, refresh_token


def get_user_by_id(id: int):
    """根据用户ID来获取用户模型对象"""
    return User.query.get(id)


def del_token(id: int):
    """删除token"""
    cache.delete(f"access_token_{id}")  # cache即redis_cache，上面导包时起了别名


class UploadFileError(Exception):
    """
    上传文件失败
    """
    pass


def save_avatar(img: str, ext: str) -> str:
    """保存用户头像"""
    b64_avatar = img[img.find(",") + 1:]  # 获取base64编码的头像数据
    b64_image = base64.b64decode(b64_avatar)  # 讲base64编码的头像数据解码成二进制数据
    file_name = uuid.uuid4()

    file = f"{current_app.config['AVATAR_URL']}/{file_name}.{ext}"
    ret = oss.upload(file, b64_image)

    if ret.status != 200:
        raise UploadFileError()
    url = f"{oss.bucket_url}/{file}"
    return url


def update_user(user: User, data: Dict):
    """更新用户信息"""
    for k, v in data.items():
        setattr(user, k, v)
    mysqldb.session.commit()

from typing import Dict, Any, Tuple

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token

from application import redis_cache as cache
from .models import User


def gen_token(payload: Dict[str, Any]) -> Tuple:
    """生成access_token和refresh_token"""
    access_token: str = create_access_token(identity=payload)  # identity 就是载荷
    refresh_token: str = create_refresh_token(identity=payload)
    # 缓存一个token到redis中，表示当前用户在服务端的登录状态，将来如果token或者删除数据库中用户信息时，会删除调用当前redis中保存的token
    cache.setex(f"access_token_{payload['id']}", current_app.config["JWT_ACCESS_TOKEN_EXPIRES"], access_token)

    return access_token, refresh_token


def get_user_by_id(id: int):
    """根据用户ID来获取用户模型对象"""
    return User.query.get(id)

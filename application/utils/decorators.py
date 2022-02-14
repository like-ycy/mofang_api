from typing import Callable, Any, Union, Dict

from application import code, message
from flask_jwt_extended import get_jwt_identity, jwt_required


def get_user_object(func: Callable) -> Callable:
    """用户鉴权，并获取用户模型对象"""

    @jwt_required()  # 验证jwt
    def wrapper(*args, **kwargs) -> Union[Callable, Dict[str, Any]]:
        from application.apps.users.models import User
        payload = get_jwt_identity()
        user_id = int(payload["id"])
        user = User.query.filter(User.id == user_id).first()
        if user is None:
            return {
                "errno": code.CODE_USER_NOT_EXISTS,
                "errmsg": message.USER_NOT_EXISTS
            }
        return func(user, *args, **kwargs)

    return wrapper

from typing import Dict, Union

from application import message, code
from .serializers import MobileSchema, ValidationError


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

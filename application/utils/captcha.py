import json
from typing import NoReturn, Dict, Any
from urllib.parse import urlencode
from urllib.request import urlopen

from flask import current_app


class CaptchaError(Exception):
    """验证码异常"""
    pass


class CaptchaParamsError(CaptchaError):
    """参数异常"""
    pass


class CaptchaNetWorkError(CaptchaError):
    """网络异常"""
    pass


class CaptchaFailError(CaptchaError):
    """验证失败"""
    pass


def check_captcha(ticket: str, randstr: str, user_ip: str) -> NoReturn:
    """防水墙验证码的验证回调方法"""

    if len(ticket) < 1 or len(randstr) < 1:
        raise CaptchaParamsError

    try:
        params: Dict[str, Any] = {
            "aid": current_app.config.get("CAPTCHA_APP_ID"),
            "AppSecretKey": current_app.config.get("CAPTCHA_APP_SECRET_KEY"),
            "Ticket": ticket,
            "Randstr": randstr,
            "UserIP": user_ip
        }
    except Exception:
        raise CaptchaParamsError

    try:
        # aid=xxx&appsecretkey=xxx&
        params: bytes = urlencode(params).encode(encoding="utf-8")
        content: bytes = urlopen(current_app.config.get("CAPTCHA_GATEWAY"), params).read()
        res: Dict[str, Any] = json.loads(content)
    except:
        raise CaptchaNetWorkError

    if res["response"] != '1':
        raise CaptchaFailError

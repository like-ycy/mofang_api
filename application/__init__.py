"""项目初始化主程序"""
from flask import Flask


def init_app() -> Flask:
    """初始化Flask应用"""
    app: Flask = Flask(__name__)
    return app

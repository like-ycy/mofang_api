"""项目初始化主程序"""
from flask import Flask

from application.utils.config import Config

# 初始化配置类
config: Config = Config()


def init_app(config_path) -> Flask:
    """初始化Flask应用"""
    app: Flask = Flask(__name__)
    config.init_app(app, config_path)
    return app

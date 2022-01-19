"""项目初始化主程序"""
from pathlib import Path

from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from application.utils import message, code
from application.utils.blueprint import register_blueprint, path
from application.utils.commands import Command
from application.utils.config import Config
from application.utils.logger import Logger

# 初始化配置类
config: Config = Config()

# SqlAlchemy实例化
mysqldb: SQLAlchemy = SQLAlchemy()

# Redis实例化
redis_cache: FlaskRedis = FlaskRedis(config_prefix='REDIS')
redis_check: FlaskRedis = FlaskRedis(config_prefix='CHECK')

# mongoDB实例化
mongo: PyMongo = PyMongo()

# 日志实例化
log = Logger()

# 自定义命令实例化
command: Command = Command()

# jsonrpc实例化
jsonrpc = JSONRPC()


def init_app(config_path) -> Flask:
    """初始化Flask应用"""
    app: Flask = Flask(__name__)
    # 项目跟目录路径
    app.BASE_DIR = Path(__file__).resolve().parent.parent
    config.init_app(app, config_path)
    mysqldb.init_app(app)
    redis_cache.init_app(app)
    redis_check.init_app(app)
    mongo.init_app(app)
    log.init_app(app)
    command.init_app(app)
    # jsonrpc注册到项目中
    # 开启rpc接口的web调试界面：/api/browse
    jsonrpc.browse_url = app.config.get("API_BROWSE_URL", "/api/browse")
    jsonrpc.enable_web_browsable_api = app.config.get("DEBUG", False)
    jsonrpc.init_app(app)
    register_blueprint(app, jsonrpc)  # 注册蓝图
    with app.app_context():
        mysqldb.create_all()  # db创建数据表
    return app

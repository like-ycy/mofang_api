"""项目初始化主程序"""
from pathlib import Path

from celery import Celery
from faker import Faker
from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from application.utils import message, code
from application.utils.blueprint import register_blueprint, path, APIView
from application.utils.commands import Command
from application.utils.config import Config
from application.utils.logger import Logger
from flask_jwt_extended import JWTManager

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

# celery初始化
celery = Celery()

# jwt认证模块实例化
jwt = JWTManager()


def init_app(config_path) -> Flask:
    """初始化Flask应用"""
    app: Flask = Flask(__name__)

    # 项目跟目录路径
    app.BASE_DIR = Path(__file__).resolve().parent.parent

    # 初始化flask配置
    config.init_app(app, config_path)

    # 初始化SqlAlchemy配置
    mysqldb.init_app(app)

    # 初始化Redis配置(配置了2个库)
    redis_cache.init_app(app)
    redis_check.init_app(app)

    # 初始化mongoDB配置
    mongo.init_app(app)

    # 初始化日志配置
    log.init_app(app)

    # 初始化自定义命令
    command.init_app(app)

    # jsonrpc注册到项目中
    # 开启rpc接口的web调试界面：/api/browse
    jsonrpc.browse_url = app.config.get("API_BROWSE_URL", "/api/browse")
    jsonrpc.enable_web_browsable_api = app.config.get("DEBUG", False)
    jsonrpc.init_app(app)

    # jwt初始化，必须写在蓝图注册代码的上方
    jwt.init_app(app)

    # 注册蓝图
    register_blueprint(app, jsonrpc)

    # 数据种子生成器[faker]
    app.faker = Faker(app.config.get("LANGUAGE"))

    # 加载celery配置
    celery.main = app.name
    celery.app = app
    # 更新配置
    celery.conf.update(app.config)
    # 自动注册任务
    celery.autodiscover_tasks(app.config.get("INSTALL_BLUEPRINT"))

    # 启动项目自动根据模型建表
    with app.app_context():
        mysqldb.create_all()  # db创建数据表
    return app

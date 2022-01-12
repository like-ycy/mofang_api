"""项目初始化主程序"""
from flask import Flask
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from application.utils.config import Config

# 初始化配置类
config: Config = Config()

# SqlAlchemy实例化
mysqldb: SQLAlchemy = SQLAlchemy()

# Redis实例化
redis_cache: FlaskRedis = FlaskRedis(config_prefix='REDIS')
redis_check: FlaskRedis = FlaskRedis(config_prefix='CHECK')

# mongoDB实例化
mongo: PyMongo = PyMongo()


def init_app(config_path) -> Flask:
    """初始化Flask应用"""
    app: Flask = Flask(__name__)
    config.init_app(app, config_path)
    mysqldb.init_app(app)
    redis_cache.init_app(app)
    redis_check.init_app(app)
    mongo.init_app(app)
    return app

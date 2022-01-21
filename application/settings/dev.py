"""开发模式配置"""

# 调试模式
DEBUG: bool = True
# 语言
LANGUAGE: str = "zh_CN"

"""MySQL数据库配置"""
# 数据库连接
SQLALCHEMY_DATABASE_URI: str = "mysql://mofang_user:mofang@127.0.0.1:3306/mofang?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
# 查询时会显示原始SQL语句
SQLALCHEMY_ECHO: bool = True

"""Redis数据库配置"""
# 默认缓存数据
REDIS_URL: str = "redis://dba:123.com@127.0.0.1:6379/0"
# 验证相关缓存
CHECK_URL: str = "redis://dba:123.com@127.0.0.1:6379/1"

"""mongoDB配置"""
MONGO_URI: str = "mongodb://mofang:mofang@127.0.0.1:27017/mofang"

"""日志配置"""
LOG_FILE: str = "logs/mofang.log"
LOG_LEVEL: str = "DEBUG"
LOG_BACKPU_COUNT: int = 31
LOG_FORMAT: str = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'

"""蓝图列表(子应用)"""
INSTALL_BLUEPRINT = [
    "application.apps.users",
]

"""总路由"""
URL_PATH = "application.urls"

"""JSONRPC"""
# api接口web调试界面的url地址
API_BROWSE_URL = "/api/browse"

"""短信相关配置"""
SMS_ACCOUNT_ID: str = "8a216da863f8e6c20164139687e80c1b"  # 接口主账号
SMS_ACCOUNT_TOKEN: str = "6dd01b2b60104b3dbc88b2b74158bac6"  # 认证token令牌
SMS_APP_ID: str = "8a216da863f8e6c20164139688400c21"  # 应用ID
SMS_TEMPLATE_ID: int = 1  # 短信模板ID
SMS_EXPIRE_TIME: int = 60 * 5  # 短信有效时间，单位:秒/s
SMS_INTERVAL_TIME: int = 60  # 短信发送冷却时间，单位:秒/s

"""Celery配置"""
# 某些情况下可以防止死锁
CELERY_FORCE_EXECV = True
# 设置并发的worker数量
CELERYD_CONCURRENCY = 20
# 设置失败允许重试
CELERY_ACKS_LATE = True
# 每个worker最多执行500个任务被销毁，可以防止内存泄漏
CELERYD_MAX_TASKS_PER_CHILD = 500
# 单个任务的最大运行时间，超时会被杀死【注意：如果异步任务中有IO操作则建议不要设置这个数字太小，或者建议不要设置了】
CELERYD_TIME_LIMIT = 10 * 60
# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERY_DISABLE_RATE_LIMITS = True
# celery的任务结果内容格式
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
# celery的任务队列地址
BROKER_URL = "redis://dba:123.com@127.0.0.1:6379/15"
# celery的结果队列地址
CELERY_RESULT_BACKEND = "redis://dba:123.com@127.0.0.1:6379/14"

# celery的定时任务调度器配置
BEAT_SCHEDULE = {
    # "test": {
    #     "task": "get_sendback",
    #     "schedule": 10,
    # }
}

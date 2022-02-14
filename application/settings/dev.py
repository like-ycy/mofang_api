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

"""jwt 相关配置"""
# 加密算法,默认: HS256
JWT_ALGORITHM = "HS256"
# 秘钥，默认是flask配置中的SECRET_KEY
JWT_SECRET_KEY = "y58Rsqzmts6VCBRHes1Sf2DHdGJaGqPMi6GYpBS4CKyCdi42KLSs9TQVTauZMLMw"
# token令牌有效期，单位: 秒/s，默认:　datetime.timedelta(minutes=15) 或者 15 * 60
JWT_ACCESS_TOKEN_EXPIRES = 60 * 30
# refresh刷新令牌有效期，单位: 秒/s，默认：datetime.timedelta(days=30) 或者 30*24*60*60
JWT_REFRESH_TOKEN_EXPIRES = 30 * 24 * 60 * 60
# 设置通过哪种方式传递jwt，默认是http请求头，也可以是query_string，json，cookies
JWT_TOKEN_LOCATION = ["headers", "json", "query_string"]
# 当通过http请求头传递jwt时，请求头参数名称设置，默认值： Authorization
JWT_HEADER_NAME = "Authorization"
# 当通过http请求头传递jwt时，令牌的前缀。
# 默认值为 "Bearer"，例如：Authorization: Bearer <JWT>
JWT_HEADER_TYPE = "jwt"
# 当通过json请求体传递jwt时，access_token令牌参数名称
JWT_JSON_KEY = "access_token"
# 当通过json请求体传递jwt时，refresh_token令牌参数名称
JWT_REFRESH_JSON_KEY = "refresh_token"
# 当通过查询字符串query_string传递jwt时，地址栏的参数名称设置，默认值： Authorization
JWT_QUERY_STRING_NAME = "token"
# 当通过查询字符串query_string传递jwt时，令牌的前缀。
# 默认值为 "Bearer"，例如：Authorization: Bearer <JWT>
JWT_QUERY_STRING_VALUE_PREFIX = "jwt "

"""防水墙验证码"""
CAPTCHA_GATEWAY = "https://ssl.captcha.qq.com/ticket/verify"
CAPTCHA_APP_ID = "2071340228"
CAPTCHA_APP_SECRET_KEY = "0v714N6pMtV587ymedaJM2w**"

"""静态文件存储目录"""
# 头像存储路径
AVATAR_DIR = "application/static/avatar"
AVATAR_URL = "static/avatar"

"""阿里云"""
ALI_ACCESS_KEY_ID = "xxxxxxxx"  # 访问key
ALI_ACCESS_KEY_SECRET = "xxxxxxxx"  # 访问秘钥

# OSS对象存储
OSS_ENDPOINT = "oss-cn-beijing.aliyuncs.com"  # 存储节点
OSS_BUCKET_NAME = "mofangproject"  # 存储空间
OSS_BUCKET_URL = "https://mofangproject.oss-cn-beijing.aliyuncs.com"

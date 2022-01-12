"""开发模式配置"""

# 调试模式
DEBUG: bool = True
# 语言
LANGUAGE: str = "zh_hans"

"""MySQL数据库配置"""
# 数据库连接
SQLALCHEMY_DATABASE_URI: str = "mysql://mofang_user:mofang@127.0.0.1:3306/mofang?charset=utf8mb4"

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

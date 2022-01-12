import logging
from logging.handlers import TimedRotatingFileHandler  # 按时间分割日志文件

from flask import Flask


class Logger():
    """日志配置"""

    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        读取项目的配置项
        :param app: 当前flask应用实例对象
        :return:
        """
        self.app = app
        self.log_file = self.app.BASE_DIR / self.app.config.get("LOG_FILE", 'logs/app.log')
        self.log_level = self.app.config.get("LOG_LEVEL", 'INFO')
        self.log_backpu_count = self.app.config.get("LOG_BACKPU_COUNT", 31)
        self.log_format = self.app.config.get("LOG_FORMAT",
                                              '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

        self.setup()

    def setup(self) -> None:
        """
        集成日志功能到flask项目中
        :return:
        """
        handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
            filename=self.log_file,  # 日志存储的文件路径
            when="midnight",  # 每天备份日志的时间，午夜
            backupCount=self.log_backpu_count,  # 备份数量
            encoding='UTF-8'
        )
        # 设置日志等级
        handler.setLevel(self.log_level)
        # 设置日志格式
        logging_format: logging.Formatter = logging.Formatter(self.log_format)
        handler.setFormatter(logging_format)

        self.app.logger.addHandler(handler)

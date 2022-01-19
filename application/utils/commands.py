import os
from typing import Optional

import click
from flask import Flask


class Command():
    """自定义命令"""

    def __init__(self, app: Optional[Flask] = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app: Flask = app
        self.setup()

    def setup(self):
        """初始化终端命令"""
        self.blueprint()  # 自动创建蓝图目录和文件

    def blueprint(self):
        @self.app.cli.command("startapp")  # 指定终端命令的调用名称
        @click.option("--name", default="home", help="蓝图目录名称", type=str)
        def create_blueprint(name: str):
            # 生成蓝图名称对象的目录
            os.mkdir(name)
            open("%s/__init__.py" % name, "w")
            open("%s/views.py" % name, "w")  # 普通视图文件
            open("%s/models.py" % name, "w")
            open("%s/urls.py" % name, "w")  # 视图路由
            open("%s/serializers.py" % name, "w")  # 序列化器文件

            print("蓝图[%s]创建完成...." % name)

import os
import random
from typing import Optional

import click
from faker.providers import internet
from flask import Flask


class Command(object):
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
        self.faker()  # 自动创建faker数据

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

    def faker(self):
        # 自定义终端命令: 创建测试用户
        @self.app.cli.command("user")  # 指定终端命令的调用名称
        @click.option("--num", default="", help="用户数量")
        @click.option("--password", default="", help="登录密码")
        def faker_user(num, password):
            from application.apps.users.models import User, UserProfile
            from application import mysqldb
            faker = self.app.faker
            faker.add_provider(internet)
            try:
                num = int(num)
            except:
                num = 1
            if len(password) < 1:
                password = "123456"

            user_list = []
            for _ in range(0, num):
                sex = bool(random.randint(0, 2))
                if sex == 0:
                    # 性别保密的用户
                    nickname = faker.name()
                elif sex == 1:
                    # 性别为男的用户
                    nickname = faker.name_male()
                else:
                    # 性别为女的用户
                    nickname = faker.name_female()
                # 6~20位长度的账号
                name = faker.pystr(min_chars=6, max_chars=16)

                # 生成指定范围的时间对象
                age = random.randint(13, 50)
                birthday = faker.date_time_between(start_date="-%sy" % age, end_date="-12y", tzinfo=None)
                hometown_province = faker.province()
                hometown_city = faker.city()
                hometown_area = faker.district()
                living_province = faker.province()
                living_city = faker.city()
                living_area = faker.district()

                user = User(
                    nickname=nickname,
                    sex=sex,
                    name=name,
                    password=password,
                    money=random.randint(100, 99999),
                    credit=random.randint(100, 99999),
                    ip_address=faker.ipv4_public(),
                    email=faker.ascii_free_email(),
                    mobile=faker.phone_number(),
                    unique_id=faker.uuid4(),
                    province=faker.province(),
                    city=faker.city(),
                    area=faker.district(),
                    info=UserProfile(
                        birthday=birthday,
                        hometown_province=hometown_province,
                        hometown_city=hometown_city,
                        hometown_area=hometown_area,
                        hometown_address=hometown_province + hometown_city + hometown_area + faker.street_address(),
                        living_province=living_province,
                        living_city=living_city,
                        living_area=living_area,
                        living_address=living_province + living_city + living_area + faker.street_address()
                    )
                )

                user_list.append(user)

            mysqldb.session.add_all(user_list)
            mysqldb.session.commit()

            print(f"成功创建了{num}个用户，登录密码：{password}")

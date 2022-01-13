from typing import List

from flask import Flask, Blueprint


def register_blueprint(app: Flask):
    """自动注册蓝图(子应用)"""
    # 从配置文件中读取需要注册到项目中的蓝图路径信息
    blueprint_path_list: List = app.config.get('INSTALL_BLUEPRINT', [])
    # 遍历蓝图路径列表，对每一个蓝图进行初始化
    for blueprint_path in blueprint_path_list:
        # 获取子应用名称
        blueprint_name: str = blueprint_path.split('.')[-1]
        # 创建蓝图对象
        blueprint: Blueprint = Blueprint(blueprint_name, blueprint_path)
        # 蓝图对象注册到app
        app.register_blueprint(blueprint, url_prefix="")

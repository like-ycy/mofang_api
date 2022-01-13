from importlib import import_module
from types import ModuleType
from typing import List, Callable, Union, Dict

from flask import Flask, Blueprint


def register_blueprint(app: Flask):
    """自动注册蓝图(子应用)"""
    # 从配置文件中读取需要注册到项目中的蓝图路径信息
    blueprint_path_list: List = app.config.get('INSTALL_BLUEPRINT', [])
    # blueprint_path_list = ["application.apps.home", "application.apps.users"]

    # 从配置文件中读取总路由配置
    app_url_path: str = app.config.get('URL_PATH', 'application.urls')  # "application.urls"
    app_urls_module: ModuleType = import_module(app_url_path)
    # [{'url_prefix': '/home', 'blueprint_url_subffix': 'home.urls'}]

    # 总路由列表
    if not hasattr(app_urls_module, 'urlpatterns'):
        app.logger.error("总路由文件URL_PATH，没有路s由列表！")
        raise Exception("总路由文件URL_PATH，没有路由列表！")

    app_urlpatterns: List = app_urls_module.urlpatterns

    # 遍历蓝图路径列表，对每一个蓝图进行初始化
    for blueprint_path in blueprint_path_list:
        # 获取子应用名称
        blueprint_name: str = blueprint_path.split('.')[-1]  # "home", "users"

        # 创建蓝图对象
        blueprint: Blueprint = Blueprint(blueprint_name, blueprint_path)

        # 蓝图路由的前缀
        url_prefix: str = ""

        # 蓝图下的子路由列表
        urlpatterns: List = []

        # 获取蓝图的父级目录，目的是为了拼接总路由中所有蓝图下的urls子路由文件的路径
        blueprint_father_path: str = ".".join(blueprint_path.split(".")[:-1])  # .application.apps

        # 循环总路由列表
        for item in app_urlpatterns:
            # item = 'path("/home", "home.urls")'

            # 判断当前蓝图是否有注册到总路由中提供对外访问
            if blueprint_name in item["blueprint_url_subffix"]:
                # blueprint_name = "home.urls"

                # 导入当前蓝图下的子路由模块
                urls_module: ModuleType = import_module(f"{blueprint_father_path}.{item['blueprint_url_subffix']}")
                # url_module = import .application.apps.home.urls

                if hasattr(urls_module, "urlpatterns"):
                    # 获取子路由文件中的路由列表
                    urlpatterns: List = urls_module.urlpatterns
                    # urlpatterns = [path("/index", views.index, methods=['GET']), .....]

                # 提取蓝图路由的前缀
                url_prefix = item["url_prefix"]  # url_prefix = '/home'

                # 从总路由中查到当前蓝图对象的前缀就不要继续往下遍历了
                break

        # 把urlpatterns的每一个路由信息添加注册到蓝图对象里面
        for url in urlpatterns:
            # url = {role："/index", view_func："views.index"}
            blueprint.add_url_rule(**url)

        # 蓝图对象注册到app，url_prefix 是蓝图下所有子路由的地址前缀
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def path(rule: str, name: Union[Callable, str], **kwargs) -> Dict:
    if isinstance(name, Callable):
        return {"rule": rule, "view_func": name, **kwargs}
    elif isinstance(name, str):
        return {"url_prefix": rule, "blueprint_url_subffix": name, **kwargs}
    else:
        return {}

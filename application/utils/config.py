from flask import Flask


class Config:
    """项目配置加载类"""

    def __init__(self, app: Flask = None, config_path: str = None):
        if app:
            self.init_app(app, config_path)

    def init_app(self, app: Flask, path: str) -> None:
        """
        项目配置初始化函数
        :param app: 当前flask应用实例对象[python中的对象属于引用类型，所以函数内部改了app的数据，外界的app也会修改]
        :param path: 配置文件的导包路径   application.settings.dev
        :return:
        """
        app.config.from_object(path)

from datetime import datetime

from application import mysqldb


class BaseModel(mysqldb.Model):
    """公共模型"""
    __abstract__ = True  # 抽象模型
    id = mysqldb.Column(mysqldb.Integer, primary_key=True, comment="主键ID")
    name = mysqldb.Column(mysqldb.String(255), default="", comment="名称/标题")
    is_deleted = mysqldb.Column(mysqldb.Boolean, default=False, comment="逻辑删除")
    orders = mysqldb.Column(mysqldb.Integer, default=0, comment="排序")
    status = mysqldb.Column(mysqldb.Boolean, default=True, comment="状态(是否显示,是否激活)")
    created_time = mysqldb.Column(mysqldb.DateTime, default=datetime.now, comment="创建时间")
    updated_time = mysqldb.Column(mysqldb.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"{self.__class__.__name__} : {self.name}"

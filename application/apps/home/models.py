from application import mysqldb


class User(mysqldb.Model):
    __tablename__ = "mf_user"
    id = mysqldb.Column(mysqldb.Integer, primary_key=True, comment="主键ID")
    name = mysqldb.Column(mysqldb.String(255), unique=True, comment="账户名")
    password = mysqldb.Column(mysqldb.String(255), comment="登录密码")
    ip_address = mysqldb.Column(mysqldb.String(255), index=True, comment="登录IP")

    def __repr__(self):
        return self.name

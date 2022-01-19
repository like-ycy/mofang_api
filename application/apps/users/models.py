from werkzeug.security import generate_password_hash, check_password_hash

from application.utils.models import BaseModel, mysqldb


class User(BaseModel):
    """用户基本信息表"""

    __tablename__ = "mf_user"
    name = mysqldb.Column(mysqldb.String(255), index=True, comment="用户账户")
    nickname = mysqldb.Column(mysqldb.String(255), comment="用户昵称")
    _password = mysqldb.Column(mysqldb.String(255), comment="登录密码")
    age = mysqldb.Column(mysqldb.SmallInteger, comment="年龄")
    money = mysqldb.Column(mysqldb.Numeric(10, 2), default=0.0, comment="账户余额")
    credit = mysqldb.Column(mysqldb.Numeric(10, 2), default=0.0, comment="积分余额")
    ip_address = mysqldb.Column(mysqldb.String(255), default="", index=True, comment="登录IP")
    intro = mysqldb.Column(mysqldb.String(500), default="", comment="个性签名")
    avatar = mysqldb.Column(mysqldb.String(255), default="", comment="头像url地址")
    sex = mysqldb.Column(mysqldb.SmallInteger, default=0, comment="性别")  # 0表示未设置,保密, 1表示男,2表示女
    email = mysqldb.Column(mysqldb.String(32), index=True, default="", nullable=False, comment="邮箱地址")
    mobile = mysqldb.Column(mysqldb.String(32), index=True, nullable=False, comment="手机号码")
    unique_id = mysqldb.Column(mysqldb.String(255), index=True, default="", comment="客户端唯一标记符")
    province = mysqldb.Column(mysqldb.String(255), default="", comment="省份")
    city = mysqldb.Column(mysqldb.String(255), default="", comment="城市")
    area = mysqldb.Column(mysqldb.String(255), default="", comment="地区")
    info = mysqldb.relationship(
        "UserProfile",
        uselist=False,
        backref="user",
        primaryjoin="User.id==UserProfile.user_id",
        foreign_keys="UserProfile.user_id",
    )

    # 存取器
    @property
    def password(self):  # user.password
        return self._password

    @password.setter
    def password(self, rawpwd):  # user.password = '123456'
        """密码加密"""
        self._password = generate_password_hash(rawpwd)

    def check_password(self, rawpwd):
        """验证密码"""
        return check_password_hash(self.password, rawpwd)


class UserProfile(BaseModel):
    """用户详情信息表"""

    __tablename__ = "mf_user_profile"
    user_id = mysqldb.Column(mysqldb.Integer, index=True, comment="用户ID")
    education = mysqldb.Column(mysqldb.Integer, comment="学历教育")
    middle_school = mysqldb.Column(mysqldb.String(255), default="", comment="初中/中专")
    high_school = mysqldb.Column(mysqldb.String(255), default="", comment="高中/高职")
    college_school = mysqldb.Column(mysqldb.String(255), default="", comment="大学/大专")
    profession_cate = mysqldb.Column(mysqldb.String(255), default="", comment="职业类型")
    profession_info = mysqldb.Column(mysqldb.String(255), default="", comment="职业名称")
    position = mysqldb.Column(mysqldb.SmallInteger, default=0, comment="职位/职称")
    emotion_status = mysqldb.Column(mysqldb.SmallInteger, default=0, comment="情感状态")
    birthday = mysqldb.Column(mysqldb.DateTime, default="", comment="生日")
    hometown_province = mysqldb.Column(mysqldb.String(255), default="", comment="家乡省份")
    hometown_city = mysqldb.Column(mysqldb.String(255), default="", comment="家乡城市")
    hometown_area = mysqldb.Column(mysqldb.String(255), default="", comment="家乡地区")
    hometown_address = mysqldb.Column(mysqldb.String(255), default="", comment="家乡地址")
    living_province = mysqldb.Column(mysqldb.String(255), default="", comment="现居住省份")
    living_city = mysqldb.Column(mysqldb.String(255), default="", comment="现居住城市")
    living_area = mysqldb.Column(mysqldb.String(255), default="", comment="现居住地区")
    living_address = mysqldb.Column(mysqldb.String(255), default="", comment="现居住地址")

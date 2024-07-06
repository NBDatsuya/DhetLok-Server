# 模型类：用户信息

from external_utils import db


class UserInfo(db.Model):
    id = db.Column(db.BigInteger(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.SmallInteger(), nullable=False)
    deleted = db.Column(db.SmallInteger(), nullable=False)

    def __init__(self, username, password, role=0, deleted=0):
        self.username = username
        # self.pwd = generate_password_hash(pwd)   使用密码哈希存储密码
        self.password = password
        self.role = role
        self.deleted = deleted

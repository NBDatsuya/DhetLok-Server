from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = 'some_secret_key'

# 配置连接
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:root@localhost:3306/dhetlok'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


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


@app.route('/')
def hello():
    return jsonify(
        {
            "code": 0,
            "msg": "欢迎欢迎",
            "data": {}
        }
    ), 200


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    # hashed_pwd = generate_password_hash(password)
    try:
        user = UserInfo(
            username=username,  # 用户名
            password=password,  # 对密码加密
        )
        db.session.add(user)  # 添加数据
        db.session.commit()  # 提交数据

        return jsonify({
            "code": 0,
            "msg": "请求成功",
            "data": {}
        }), 200

    except Exception as e:
        db.session.rollback()  # 回滚，错误操作全部撤销
        return jsonify({
            "code": 1,
            "msg": "请求失败，原因：{}".format(e),
            "data": {}
        }), 200


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = UserInfo.query.filter_by(
        username=username,
        password=password,
        deleted=0
    ).first()

    # if user and check_password_hash(user['pwd'], pwd):
    if user:
        session['user_id'] = user.id
        return jsonify({
            "code": 0,
            "msg": "请求成功",
            "data": {
                "id": user.id,
                "username": user.username,
            }
        }), 200
    else:
        return jsonify({
            "code": 1,
            "msg": "登陆失败，用户名或密码错误",
            "data": {}
        }), 200


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({
        "code": 0,
        "msg": "请求成功",
        "data": {}
    }), 200


@app.teardown_appcontext
def close_connection(exception):
    db.session.close()

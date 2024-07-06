from external_utils import Blueprint, request, db, jsonify, session
from model.user import UserInfo

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


@user_bp.route('/register', methods=['POST'])
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


@user_bp.route('/login', methods=['POST'])
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


@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({
        "code": 0,
        "msg": "请求成功",
        "data": {}
    }), 200

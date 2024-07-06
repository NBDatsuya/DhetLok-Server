from external_utils import Blueprint, request, db, jsonify, session
from model.user import UserInfo

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


@user_bp.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    # hashed_pwd = generate_password_hash(password)

    # 判断用户名是否存在
    user = UserInfo.query.filter_by(username=username).first()
    if user:
        return jsonify({
            "code": 1,
            "msg": "注册失败，该用户已存在",
            "data": {}
        }), 200

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
        deleted=0,
        role=0
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
                "role": user.role
            }
        }), 200
    else:
        return jsonify({
            "code": 1,
            "msg": "登陆失败，用户名或密码错误",
            "data": {}
        }), 200


@user_bp.route('/admin-login', methods=['POST'])
def admin_login():
    username = request.json['username']
    password = request.json['password']

    user = UserInfo.query.filter_by(
        username=username,
        password=password,
        deleted=0,
        role=1
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
                "role": user.role
            }
        }), 200
    else:
        return jsonify({
            "code": 1,
            "msg": "登陆失败，用户名或密码错误",
            "data": {}
        }), 200


@user_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({
        "code": 0,
        "msg": "请求成功",
        "data": {}
    }), 200


@user_bp.route('/modify-password', methods=['POST'])
def modify_password():
    user = request.form.get("id")
    old_pwd = request.form.get("old")
    new_pwd = request.form.get("new")
    # 检查原始密码是否正确
    user = UserInfo.query.filter_by(id=user).first()  # 获取用户信息
    res = {}
    if not user.password == old_pwd:
        res['code'] = 1
        res['msg'] = '密码修改错误：旧密码输入错误'
        return jsonify(res)
    # 更改密码
    try:
        user.password = new_pwd
        db.session.add(user)
        db.session.commit()

        res['code'] = 0
        res['msg'] = '密码修改成功'
        return jsonify(res)
    except Exception as e:
        res['code'] = -1
        res['msg'] = '密码修改错误，原因{}'.format(e)
        return jsonify(res)


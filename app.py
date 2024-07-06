from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = 'some_secret_key'

app.config['JSON_AS_ASCII'] = False  # 解决中文乱码问题
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

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    artist_name = db.Column(db.String(100))  # 歌手名
    style = db.Column(db.Integer)  # 歌手类型
    img_url = db.Column(db.Text)  # 头像
    hot = db.Column(db.Boolean, default=0)  # 是否热门
class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    song_name = db.Column(db.String(100))  # 歌曲名称
    singer = db.Column(db.String(100))  # 歌手名称
    file_url = db.Column(db.String(100))  # 歌曲图片
    hits = db.Column(db.Integer, default=0)  # 点击量
    style = db.Column(db.Integer)  # 歌曲类型 0：全部 1:华语 2：欧美 3：日语 4：韩语 5 其他
    collect = db.relationship('Collect', backref='song')  # 收藏外键关系关联
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

#获取所有歌手信息
@app.route('/api/getartists', methods=['GET'])
def get_artists():
    artists = Artist.query.all()
    artist_list = []
    for artist in artists:
        artist_data = {
            'id': artist.id,
            'artist_name': artist.artist_name,
            'style': artist.style,
            'img_url': artist.img_url,
            'hot': artist.hot
        }
        artist_list.append(artist_data)
    return jsonify(artist_list)

#根据“singer”（歌手）名称模糊查询song_name（歌曲名称）并显示
@app.route('/api/searchsong', methods=['GET'])
def search_songs():
    singer = request.args.get('singer', '')
    # 支持模糊查询，如果仅输入一个字，则使用该字作为前缀
    if len(singer) == 1:
        songs = Song.query.filter(Song.singer.like(f'{singer}%')).all()
    else:
        songs = Song.query.filter(Song.singer == singer).all()

    songs_list = [{
        'id': song.id,
        'song_name': song.song_name,
        'singer': song.singer,
        'file_url': song.file_url,
        'hits': song.hits,
        'style': song.style
    } for song in songs]
    return jsonify(songs_list)

# 获取为id的歌曲信息
@app.route('/api/getsong/<int:id>', methods=['GET'])
def get_song(id):
    song = Song.query.get(id)
    if song:
        song_data = {
            'id': song.id,
            'song_name': song.song_name,
            'singer': song.singer,
            'file_url': song.file_url,
            'hits': song.hits,
            'style': song.style
        }
        return jsonify(song_data)
    else:
        return jsonify({'message': 'Song not found'})

# 添加歌曲信息
@app.route('/api/addsong', methods=["POST"])
def add_song():
    try:
        data = request.get_json()
        print(data)
        song = Song(
            song_name=data['song_name'],
            singer=data['singer'],
            file_url=data['file_url'],  # 注意：这里假设是文件URL或链接，根据实际需求调整
            hits=data.get('hits', 0),  # 使用get方法提供默认值，以防hits未提供
            style=data['style']
        )
        db.session.add(song)
        db.session.commit()

        return jsonify({'status': 1, 'message': 'Song added successfully'})
    except Exception as e:
        print(e)
        return jsonify({'status': 0, 'message': 'Failed to add song'})

# 更新歌曲信息
@app.route('/api/updatesong/<int:id>', methods=['POST'])
def update_song(id):
    song = Song.query.get(id)
    if song:
        song_data = request.get_json()
        if 'song_name' in song_data:
            song.song_name = song_data['song_name']
        if 'singer' in song_data:
            song.singer = song_data['singer']
        if 'file_url' in song_data:
            song.file_url = song_data['file_url']
        if 'hits' in song_data:
            song.hits = song_data['hits']
        if 'style' in song_data:
            song.style = song_data['style']
        db.session.commit()
        return jsonify({'message': 'Song updated successfully'})
    else:
        return jsonify({'message': 'Song not found'})

@app.teardown_appcontext
def close_connection(exception):
    db.session.close()

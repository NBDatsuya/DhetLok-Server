import os
import time

from external_utils import Blueprint, jsonify, send_file, request, db
from model.song import Song

song_bp = Blueprint("song", __name__, url_prefix="/api/song")

SONG_PATH = "static/music/"


@song_bp.route("/all")
def get_all():
    songs = Song.query.all()

    return jsonify({
        "data": [song.to_dict() for song in songs], "code": 0, "msg": "请求成功"
    })


@song_bp.route(rule="/top/<int:limit>", methods=["GET"])
def top(limit):
    songs = Song.query.order_by(Song.hits.desc()).limit(limit=limit).all()

    return jsonify({
        "data": [song.to_dict() for song in songs], "code": 0, "msg": "请求成功"
    })


@song_bp.route(rule="/<string:file_name>", methods=["GET"])
def get_song_file(file_name):
    return send_file("{}/{}"
                     .format(SONG_PATH, file_name), mimetype="audio/mpeg")


@song_bp.route(rule="/genre/<int:genre>", methods=["GET"])
def get_by_genre(genre):
    songs = Song.query.filter_by(genre=1).order_by(Song.hits.desc()).all()

    return jsonify({
        "data": [song.to_dict() for song in songs], "code": 0, "msg": "请求成功"
    })


@song_bp.route('/search')
def search():
    keyword = request.args.get('keyword')  # 获取关键字
    page = request.args.get('page', type=int)  # 获取页数

    if keyword:
        keyword = keyword.strip()
        songs = (Song.query
                 .filter(Song.songName.like('%' + keyword + '%'))
                 .order_by(Song.hits.desc())
                 .paginate(page=page, per_page=10))
    else:
        songs = (Song.query
                 .order_by(Song.hits.desc())
                 .paginate(page=page, per_page=10))

    return jsonify({
        "code": 0, "msg": "请求成功",
        "data": [song.to_dict() for song in songs]
    })


@song_bp.route("/add", methods=["POST"])
def add_song():
    form = request.form.to_dict()
    '''
    songName = request.form.get("songName")
    singer = request.form.get("singer")
    style = request.form.get("style")
    fileURL = request.form.get("fileURL")
    '''
    try:
        # 为Song类属性赋值
        song = Song(
            real_name=form["real_name"],  # 歌曲名称
            artist=form["artist"],
            genre=form['genre'],  # 歌曲类型
            file_url=form['fileUrl']  # 文件路径
        )

        db.session.add(song)  # 添加数据
        db.session.commit()  # 提交数据

        res = {'code': 0, 'msg': '添加成功'}
    except Exception as e:
        res = {'code': -1, 'msg': '添加失败：{}'.format(e)}
    return jsonify(res)


@song_bp.route("/edit", methods=["POST"])
def edit_song():
    form = request.form.to_dict()
    song = Song.query.filter_by(id=form["id"]).first()

    # 更改Song表
    real_name = form.get("realName")
    artist = form.get("artist")
    genre = form.get("genre")
    try:
        song.real_name = real_name
        song.artist = artist
        song.genre = int(genre)
        db.session.add(song)  # 添加数据
        db.session.commit()  # 提交数据

        res = {'code': 0, 'msg': '保存成功'}
    except:
        res = {'code': 1, 'msg': '保存失败'}
    return jsonify(res)


@song_bp.route("/del")
def delete_song():
    id = request.args.get('id')  # 获取ID
    try:
        song = Song.query.get_or_404(int(id))
        db.session.delete(song)
        db.session.commit()
        res = {'code': 0, 'msg': '删除成功'}
    except Exception as e:
        res = {'code': 1, 'msg': '删除失败，原因：{}'.format(e)}
    return jsonify(res)


@song_bp.route("/upload", methods=["POST"])
def upload_song():
    file_obj = request.files.get("file")
    if file_obj is None:
        res = {'code': 1, 'msg': "上传失败，文件为空"}
        return jsonify(res)

    path = str(int(time.time())) + ".mp3"
    file_obj.save(os.path.join("../static/music", path))

    res = {'code': 0, 'msg': "上传成功", "data": path}
    return jsonify(res)


@song_bp.route("/hit/<int:song>", methods=["POST"])
def hit_plus(song):
    song = Song.query.get_or_404(song)
    if not song:
        res = {'code': 1, 'msg': '歌曲不存在'}
    # 更改点击量
    else:
        song.hits += 1
        db.session.add(song)
        db.session.commit()
        res = {'code': 0, 'msg': '请求成功，播放次数加1'}
    return jsonify(res)

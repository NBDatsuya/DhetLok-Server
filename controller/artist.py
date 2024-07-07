import os
import time

from external_utils import Blueprint, jsonify, send_file, request, db
from model.artist import Artist
from model.song import Song
from util.util import to_dict

artist_bp = Blueprint("artist", __name__, url_prefix="/api/artist")


@artist_bp.route("/info/all", methods=["GET"])
def get_all():
    artists = Artist.query.all()

    return jsonify({
        "data": [to_dict(artist) for artist in artists], "code": 0, "msg": "请求成功"
    })


@artist_bp.route("/hot/<int:limit>", methods=["GET"])
def get_hot(limit):
    artists = Artist.query.filter_by(hot=1).limit(limit=limit).all()

    return jsonify({
        "data": [to_dict(artist) for artist in artists], "code": 0, "msg": "请求成功"
    })


@artist_bp.route("/avatar/<string:file_name>", methods=["GET"])
def get_avatar(file_name):
    try:
        return send_file("static/avatar/{}".format(file_name), mimetype="image/png")
    except Exception as e:
        return jsonify({
            "data": {},
            "code": 1,
            "msg": "请求失败：{}".format(str(e))
        })


@artist_bp.route("/info/<int:artist_id>", methods=["GET"])
def get_by_id(artist_id):
    song = (Song.query
            .join(Artist, Song.artist == Artist.real_name)
            .filter(Artist.id == artist_id)
            .all())
    artist = (Artist.query.filter(Artist.id == artist_id).first())
    return jsonify({
        "code": 0, "msg": "请求成功",
        "data": {
            "songs": [to_dict(song) for song in song],
            "artist": to_dict(artist)
        }
    })


@artist_bp.route("/add", methods=["POST"])
def add_artist():
    real_name = request.form.get("realName")
    genre = request.form.get("genre")
    img_url = request.form.get("imgUrl")
    hot = request.form.get("hot")

    # 判断歌手是否存在
    artist = Artist.query.filter_by(real_name=real_name).first()
    if artist:
        return jsonify({'code': 1, 'msg': '该歌手已存在'})

    try:
        # 为Artist类属性赋值
        artist = Artist(
            real_name=real_name,
            genre=int(genre),
            img_url=img_url,
            hot=int(hot)
        )
        db.session.add(artist)  # 添加数据
        db.session.commit()  # 提交数据

        return {'code': 0, 'msg': '添加成功'}

    except Exception as e:
        return jsonify({
            'code': 1,
            'msg': '添加失败，原因：{}'.format(str(e))
        })


@artist_bp.route("/edit", methods=["POST"])
def edit_artist():
    artist_id = request.values['id']
    real_name = request.form.get("realName")
    genre = request.form.get("genre")
    hot = request.form.get("hot")

    artist = Artist.query.filter_by(id=artist_id).first()
    try:
        artist.real_name = real_name
        artist.genre = int(genre)
        artist.hot = int(hot)

        db.session.add(artist)  # 添加数据
        db.session.commit()  # 提交数据

        res = {'code': 0, 'msg': '保存成功'}
    except Exception as e:
        res = {'code': 1, 'msg': '保存失败，原因：{}'.format(str(e))}
    return jsonify(res)


@artist_bp.route("/del", methods=["POST"])
def delete_artist():
    id = request.args.get('id')
    try:
        artist = Artist.query.filter_by(id=id).first()

        db.session.delete(artist)
        db.session.commit()

        res = {'code': 0, 'msg': '删除成功'}
    except Exception as e:
        res = {'code': 1, 'msg': '删除失败，原因：{}'.format(str(e))}
    return jsonify(res)


@artist_bp.route("/avatar/upload", methods=["POST"])
def upload_avatar():
    file_obj = request.files.get("file")
    if file_obj is None:
        return "文件上传为空"

    path = str(int(time.time())) + ".jpg"
    file_obj.save(os.path.join("../static/music", path))

    res = {'code': 0, 'data': path, 'msg': "上传成功"}
    return jsonify(res)

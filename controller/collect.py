from external_utils import Blueprint, jsonify, request, db
from model.collect import Collect
from util.util import to_dict

collect_bp = Blueprint("collect", __name__, url_prefix="/api/collect")


@collect_bp.route("/do/<int:song>", methods=["POST"])
def do_collect(song):
    user = request.args.get("user")
    collect_info = Collect.query.filter_by(  # 根据用户ID和景区ID判断是否该收藏
        owner=int(user),
        song=int(song)
    ).first()
    res = {}
    # 已收藏
    if collect_info:
        res['code'] = 0
        res['msg'] = '已经收藏'
        res['data'] = False
    # 未收藏，进行收藏
    else:
        collect_info = Collect(
            owner=int(user),
            song=int(song)
        )
        db.session.add(collect_info)  # 添加数据
        db.session.commit()  # 提交数据

        res['code'] = 0
        res['msg'] = '收藏成功'
        res['data'] = True
    return jsonify(res)  # 返回json数据


@collect_bp.route("/my-collect/<int:owner>")
def owner_collect(owner):
    page = request.args.get('page', type=int)  # 获取page参数值
    page_data = (Collect.query
                 .filter_by(owner=owner)
                 .paginate(page=page, per_page=10))
    res = {'code': 0, 'msg': '收藏成功', 'data': [to_dict(data) for data in page_data]}
    return jsonify(res)  # 可能有bug

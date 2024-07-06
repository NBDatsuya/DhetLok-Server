from controller import blueprint_list
from external_utils import db, Flask, CORS, jsonify
import config
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = 'some_secret_key'

app.config.from_object(config)
db.init_app(app)

# 导入所有蓝图
for bp in blueprint_list:
    app.register_blueprint(bp)


@app.teardown_appcontext
def close_connection(exception=None):
    db.session.close()


@app.route('/')
def hello():
    return jsonify(
        {
            "code": 0,
            "msg": "欢迎欢迎",
            "data": "当你看到这条消息的时候，说明DhetLok的后端正在运行"
        }
    ), 200

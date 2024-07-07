import config
from controller import blueprint_list
from external_utils import db, Flask, CORS, jsonify, Swagger
from util.util import auto_swag_blueprint

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = 'some_secret_key'

app.config.from_object(config)
db.init_app(app)
swagger = Swagger(app)

# 导入所有蓝图，并生成文档
for bp in blueprint_list:
    app.register_blueprint(bp)
    auto_swag_blueprint(app, bp)


@app.teardown_appcontext
def close_connection(exception=None):
    db.session.close()


@app.route('/')
def hello():
    """
       A simple endpoint for testing
       ---
       tags:
         - Hello
       responses:
         200:
           description: Returns a hello message
           examples:
             application/json: {"message": "Hello, World!"}
       """
    return jsonify(
        {
            "code": 0,
            "msg": "欢迎欢迎",
            "data": "当你看到这条消息的时候，说明DhetLok的后端正在运行"
        }
    ), 200

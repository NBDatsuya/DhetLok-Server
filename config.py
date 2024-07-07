# 配置文件

JSON_AS_ASCII = False,  # 不转换成ASCII
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/dhetlok'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SWAGGER = {
    'title': 'DhetLok API',
    'description': 'API文档',
    'version': '1.0.0',
    'uiversion': 3
}

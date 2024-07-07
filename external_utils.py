# 外部引用
# 统一导入并管理外部库，解决了循环引用的问题

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask import send_file
from flasgger import Swagger
from flasgger.utils import swag_from
import inspect

# 配置一个“未绑定当前app的”SQLAlchemy实例
db = SQLAlchemy()

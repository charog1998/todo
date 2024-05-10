# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from init_app.settings import BASE_DIR
from flask_migrate import Migrate

migrate = Migrate()

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # 默认使用 init_app/settings.py 文件作为配置文件
        CONFIG_PATH = BASE_DIR / 'init_app/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # 如果传入了test_config，则以其为配置
        app.config.from_mapping(test_config)

    # 将SQLAlchemy实例注册到Flask实例上
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册视图
    register_bp(app)

    # 注册模型
    from app.plan import models
    from app.auth import models 
    return app


def register_bp(app:Flask):
    # 注册视图方法
    from app.plan import views as plan
    from app.auth import views as auth
    app.register_blueprint(plan.bp) 
    # 注册蓝图
    app.register_blueprint(auth.bp) 

    # 相当于设置首页为 /index
    # 即访问'/'时会定向到'/index'
    # 使用的视图函数是 plan.index
    app.add_url_rule(rule='/', endpoint='index', view_func=plan.index)
# -*- coding: utf-8 -*-
from init_app import create_app,db

def init_db():
    '''
    用于初始化数据库
    '''
    app=create_app()
    with app.app_context():
        db.create_all()

if __name__ == "__main__":


    # 初始化数据库，第一次运行时要首先运行
    # init_db()

    # # 启动Flask
    app=create_app()
    app.run('0.0.0.0',7788) # 开放到公网访问
    # # app.run('127.0.0.1',7788) # 仅限本地访问

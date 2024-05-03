# -*- coding: utf-8 -*-
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = 'HzQepvVHVXdnFuFQB0h0SIVBdEXm9kcxi4FbZ9hxXOGA20cf+utkfpMJuoQ/3kQQ'

# SQLALCHEMY_DATABASE_URI = 'mysql://用户名:密码@主机名/database' # MySQL连接时使用
# SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/todo_mysql'
SQLALCHEMY_DATABASE_URI = 'sqlite:///./tmp copy.db'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
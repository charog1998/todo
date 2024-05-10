# -*- coding: utf-8 -*-
from pathlib import Path
from urllib.parse import quote_plus as urlquote

BASE_DIR = Path(__file__).resolve().parent.parent  # 获取此文件所在的文件夹的上一级路径

DEBUG = True

SECRET_KEY = "HzQepvVHVXdnFuFQB0h0SIVBdEXm9kcxi4FbZ9hxXOGA20cf+utkfpMJuoQ/3kQQ"  # 设置密钥，用于加密 session 数据、cookie、消息闪现等敏感信息

# MySQL连接时使用
# SQLALCHEMY_DATABASE_URI = 'mysql://用户名:密码@主机名/database' 

# MySQL连接时使用，当密码中有特殊字符可使用url编码
# SQLALCHEMY_DATABASE_URI = f'mysql://用户名:{urlquote(密码)}@主机名/database' 

# 使用sqlite连接
SQLALCHEMY_DATABASE_URI = "sqlite:///./tmp copy.db"  

# SQLALCHEMY_COMMIT_ON_TEARDOWN is deprecated. 
# It can cause various design issues that are difficult to debug.
# Call db.session.commit() directly instead.
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True

SQLALCHEMY_TRACK_MODIFICATIONS = False # 用于自动追踪对数据库对象的修改并发送信号给应用程序，默认值就是False

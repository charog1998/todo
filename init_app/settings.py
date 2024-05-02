from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = 'l%3ya7fn3moipdpcltj(tdfcv5^@lj=t5d&72levvls+y*@_4^'

# SQLALCHEMY_DATABASE_URI = 'mysql://用户名:密码@主机名/database'
# SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/todo_mysql'
SQLALCHEMY_DATABASE_URI = 'sqlite:///./tmp.db'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
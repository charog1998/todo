# -*- coding: utf-8 -*-
from datetime import datetime
from init_app import db

class BaseModel(db.Model):
    """基类模型
    """
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=True, default=datetime.now) # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=True) # 更新时间


class User(BaseModel):
    """用户模型
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(320), nullable=False)

    def __repr__(self):
        return '<User: %r>' % self.username
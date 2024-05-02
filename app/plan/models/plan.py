from datetime import datetime
from init_app import db

class BaseModel(db.Model):
    """基类模型
    """
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=True, default=datetime.now) # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=True) # 更新时间


class PlanList(BaseModel):
    """大目标
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False) # 标题
    description = db.Column(db.String(240), nullable=False) # 描述
    startTime = db.Column(db.DateTime, nullable=False) # 开始时间
    deadLineTime = db.Column(db.DateTime, nullable=False) # 结束时间
    createBy = db.Column(db.Integer, nullable=False) # 创建人

    def __repr__(self):
        return '<Title: %r>' % self.title
    
class Plan(BaseModel):
    """小目标
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False) # 标题
    description = db.Column(db.String(240), nullable=False) # 描述
    startTime = db.Column(db.DateTime, nullable=False) # 开始时间
    deadLineTime = db.Column(db.DateTime, nullable=False) # 结束时间
    completedStatus = db.Column(db.Integer, nullable=False) # 是否已完成：1、已完成；0、未完成
    createBy = db.Column(db.Integer, nullable=False) # 创建人
    belongTo = db.Column(db.Integer, nullable=False) # 属于哪个大目标

    def __repr__(self):
        return '<Title: %r>' % self.title
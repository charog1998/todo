# -*- coding: utf-8 -*-
from ..models import auth, User
from init_app import db

import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth", # 此蓝图的前缀
    template_folder="../templates", # 使用的模板文件夹
    static_folder="../static", # 使用的静态文件所在的文件夹
)


@bp.route("/register", methods=("GET", "POST"))
def register():
    # 闪现消息，用字典存储，主要是考虑存上一步的成功消息和失败消息
    flashDict = {}
    if request.method == "POST":
        # 获取表单中传递过来的值
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]

        # 初始化一个临时的error变量，用来判断是否出错
        error = None

        # 做一个简单的表单判断
        # TODO
        # 应该使用WTF库进行表单判断，后续更新下
        if not username:
            error = "请输入用户名。"
        elif not password:
            error = "请输入密码。"
        if len(username) < 3 or len(username) > 16:
            error = "用户名长度请控制在3到16个字符哦。"
        if len(password) < 6 or len(password) > 18:
            error = "密码长度请控制在6到18个字符哦。"
        if password != password2:
            error = "两次输入的密码不一致。"

        # 如果表单判断无误的话则进行注册操作
        if error is None:
            try:
                # 初始化User类
                user = User(
                    username=username, password=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()

            # 如果数据库报错的话，给出提示并回滚
            except Exception as e:
                error = f"用户名“{username}”已经被注册了。"
                db.session.rollback()

            # 如果数据库没有报错的话，更新闪现消息，并重定向至登录界面
            else:
                flashDict["success"] = "注册成功。"
                flash(flashDict)
                return redirect(url_for("auth.login"))
            
        flashDict["error"] = error
        # 消息闪现
        flash(flashDict)

    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    flashDict = {}
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        # 查看数据库中是否有此用户名的用户
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "用户名不存在。"
        elif not check_password_hash(user.password, password):
            error = "密码错误。"

        # 如果没出错的话，跳转至主页
        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("auth.index"))
        flashDict["error"] = error
        flash(flashDict)

    return render_template("login.html")


# 钩子函数，在每次请求前都更新一次g.user全局变量
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route("/logout")
def logout():
    # 注销
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    '''
    装饰器
    -----
    保证某些方法只有已登录用户才能访问，否则将跳转至Login页面
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

# auth的主页，会重定向到plan.index
@bp.route("/")
@login_required
def index():
    # 主页
    return redirect(url_for("plan.index"))


@bp.route("/getUserList", methods=["GET"])
@login_required
def getUserList():
    '''
    获取用户列表
    -----------
    临时使用，为了方便调试
    '''
    if session.get("user_id") == 1:
        userList = []
        result = User.query.all()
        for user in result:
            userList.append(user.username)
        return userList

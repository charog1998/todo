from ..models import auth,User
from init_app import db

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth',template_folder='../templates', static_folder='../static')



@bp.route('/register', methods=('GET', 'POST'))
def register():
    flashDict = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        error = None

        if not username:
            error = '请输入用户名。'
        elif not password:
            error = '请输入密码。'

        if len(username)<3 or len(username)>16:
            error = '用户名长度请控制在3到16个字符哦。'

        if len(password)<6 or len(password)>18:
            error = '密码长度请控制在6到18个字符哦。'
        
        if password != password2:
            error = '两次输入的密码不一致。'

        if error is None:
            try:
                user = User(username = username, password = generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                error = f"用户名“{username}”已经被注册了。"
                db.session.rollback()
            else:
                flashDict['success'] = '注册成功。'
                flash(flashDict)
                return redirect(url_for("auth.login"))
        flashDict['error'] = error
        flash(flashDict)

    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    flashDict = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter_by(username = username).first()

        if user is None:
            error = '用户名不存在。'
        elif not check_password_hash(user.password, password):
            error = '密码错误。'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('auth.index'))
        flashDict['error'] = error
        flash(flashDict)

    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id = user_id).first()

@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/')
@login_required
def index():
    # 主页
    return redirect(url_for('plan.index'))
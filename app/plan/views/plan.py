# -*- coding: utf-8 -*-
from ..models import Plan, PlanList
from app.auth.views.auth import login_required
from init_app import db

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from datetime import datetime


bp = Blueprint(
    "plan",
    __name__,
    url_prefix="/plan",
    template_folder="../templates",
    static_folder="../static",
)


@bp.route("/")
@login_required
def index():
    """
    主页
    """
    page = request.args.get("page", 1, type=int)

    # 查询出此用户创建的所有PlanList
    # 按照结束时间进行排序
    # 利用paginate进行分页，每页7条记录
    pagination = (
        PlanList.query.filter_by(createBy=session.get("user_id"))
        .order_by(PlanList.deadLineTime)
        .paginate(page=page, per_page=7, error_out=False)
    )

    # 获取到当前分页的内容pagination.items
    planList_List = pagination.items

    # 用分页器和分页内容去渲染模板
    return render_template(
        "planList.html", planLists=planList_List, pagination=pagination
    )


@bp.route("/addList", methods=(["POST"]))
@login_required
def add_list():
    flashDict = {}
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        # 对前端回传的字符串形式的时间进行格式化，转换成datetime对象用于传入数据库
        startTime = datetime.strptime(request.form["startTime"], "%Y-%m-%d").date()
        deadLineTime = datetime.strptime(
            request.form["deadLineTime"], "%Y-%m-%d"
        ).date()

        createBy = session.get("user_id")
        error = None

        # 到数据库中查重
        planList_tmp = PlanList.query.filter_by(title=title, createBy=createBy).first()

        if planList_tmp:
            error = f"此主题：“{title}”已经存在了！"
        elif not title:
            error = "标题不能为空！"
        elif startTime > deadLineTime:
            error = "结束时间不能早于起始时间！"
        if error == None:
            try:
                planList = PlanList(
                    title=title,
                    description=description,
                    startTime=startTime,
                    deadLineTime=deadLineTime,
                    createBy=createBy,
                )
                db.session.add(planList)
                db.session.commit()
            except Exception as e:
                error = f"计划列表：“{title}”添加失败。"
                db.session.rollback()
            else:
                flashDict["success"] = "添加计划列表成功"
        flashDict["error"] = error
        flash(flashDict)
    return redirect(url_for("plan.index"))


@bp.route("/delPlanList/<int:planList_id>", methods=["GET", "POST"])
@login_required
def del_list(planList_id):
    '''
    按指定的planList_id进行删除

    参数
    ----
    planList_id
        要删除的PlanList的id
    '''
    flashDict = {}
    planList = PlanList.query.filter_by(
        id=planList_id, createBy=session.get("user_id")
    ).first()
    if planList:
        db.session.delete(planList)
        db.session.commit()
        flashDict["success"] = f"{planList.title}删除成功"
        flash(flashDict)
        return redirect(url_for("plan.index"))


@bp.route("/updatePlanList/<int:planList_id>", methods=["POST"])
@login_required
def update_list(planList_id):
    '''
    按指定的planList_id进行更新删除

    参数
    ----
    planList_id
        要更新的PlanList的id

    TODO
    ----
    尝试着用update方法结果报错了，只能使用先删除再新增的方式去操作，这里应该可以优化的
    '''
    flashDict = {}
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        # 对前端回传的字符串形式的时间进行格式化，转换成datetime对象用于传入数据库
        startTime = datetime.strptime(request.form["startTime"], "%Y-%m-%d").date()
        deadLineTime = datetime.strptime(
            request.form["deadLineTime"], "%Y-%m-%d"
        ).date()
        createBy = session.get("user_id")
        error = None

        planList_tmp = PlanList.query.filter_by(
            id=planList_id, createBy=createBy
        ).first()
        if planList_tmp.title != title:
            planList_tmp2 = PlanList.query.filter_by(
                title=title, createBy=createBy
            ).first()
            if planList_tmp2:
                error = f"此主题：“{title}”已经存在了！"
        elif not title:
            error = "标题不能为空！"
        elif startTime > deadLineTime:
            error = "结束时间不能早于起始时间！"
        if error == None:
            try:
                planList = PlanList(
                    id=planList_id,
                    title=title,
                    description=description,
                    startTime=startTime,
                    deadLineTime=deadLineTime,
                    createBy=createBy,
                )
                db.session.delete(
                    PlanList.query.filter_by(
                        id=planList_id, createBy=session.get("user_id")
                    ).first()
                )
                db.session.add(planList)
                db.session.commit()
            except Exception as e:
                error = f"计划列表：“{title}”修改失败。"
                db.session.rollback()
            else:
                flashDict["success"] = "修改计划列表成功"
        flashDict["error"] = error
        flash(flashDict)
    return redirect(url_for("plan.index"))


@bp.route("/plans/<int:planList_id>")
@login_required
def sel_plans(planList_id):
    '''
    进入PlanList之后的主页，基本思路和PlanList一样，这里偷懒了
    '''
    planList = PlanList.query.filter_by(
        createBy=session.get("user_id"), id=planList_id
    ).first()
    page = request.args.get("page", 1, type=int)
    pagination = (
        Plan.query.filter_by(createBy=session.get("user_id"), belongTo=planList_id)
        .order_by(Plan.completedStatus, Plan.deadLineTime, Plan.title)
        .paginate(page=page, per_page=7, error_out=False)
    )
    plan_List = pagination.items
    return render_template(
        "plans.html", plans=plan_List, planList=planList, pagination=pagination
    )


@bp.route("/addPlan/<int:planList_id>", methods=(["POST"]))
@login_required
def add_plan(planList_id):
    '''
    新增Plan
    '''
    flashDict = {}
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        startTime = datetime.strptime(request.form["startTime"], "%Y-%m-%d").date()
        deadLineTime = datetime.strptime(
            request.form["deadLineTime"], "%Y-%m-%d"
        ).date()
        createBy = session.get("user_id")
        belongTo = planList_id

        error = None

        planList_tmp = PlanList.query.filter_by(id=planList_id).first()
        plan_tmp = Plan.query.filter_by(title=title, createBy=createBy).first()
        if plan_tmp:
            error = f"此主题：“{title}”已经存在了！"
        elif not title:
            error = "标题不能为空！"
        elif (
            startTime < planList_tmp.startTime.date()
            or deadLineTime > planList_tmp.deadLineTime.date()
        ):
            error = "计划的时间范围超过了计划列表的时间范围！"
        elif startTime > deadLineTime:
            error = "结束时间不能早于起始时间！"
        if error == None:
            try:
                plan = Plan(
                    title=title,
                    description=description,
                    startTime=startTime,
                    deadLineTime=deadLineTime,
                    createBy=createBy,
                    belongTo=belongTo,
                    completedStatus=0,
                )
                db.session.add(plan)
                db.session.commit()
            except Exception as e:
                error = f"计划：“{title}”添加失败。"
                db.session.rollback()
            else:
                flashDict["success"] = "添加计划成功"
        flashDict["error"] = error
        flash(flashDict)
    return redirect(url_for("plan.sel_plans", planList_id=planList_id))


@bp.route("/delPlan/<int:planList_id>/<int:plan_id>", methods=["GET", "POST"])
@login_required
def del_plan(planList_id, plan_id):
    '''
    删除Plan
    '''
    flashDict = {}
    plan = Plan.query.filter_by(id=plan_id, createBy=session.get("user_id")).first()
    if plan:
        db.session.delete(plan)
        db.session.commit()
        flashDict["success"] = f"{plan.title}删除成功"
        flash(flashDict)
        return redirect(
            url_for("plan.sel_plans", planList_id=planList_id, plan_id=plan_id)
        )


@bp.route("/updatePlan/<int:planList_id>/<int:plan_id>", methods=["POST"])
@login_required
def update_plan(planList_id, plan_id):
    '''
    编辑Plan
    '''
    flashDict = {}
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        startTime = datetime.strptime(request.form["startTime"], "%Y-%m-%d").date()
        deadLineTime = datetime.strptime(
            request.form["deadLineTime"], "%Y-%m-%d"
        ).date()
        createBy = session.get("user_id")
        belongTo = planList_id
        error = None

        planList_tmp = PlanList.query.filter_by(id=planList_id).first()
        plan_tmp = Plan.query.filter_by(id=plan_id, createBy=createBy).first()
        if plan_tmp.title != title:
            plan_tmp2 = Plan.query.filter_by(title=title, createBy=createBy).first()
            if plan_tmp2:
                error = f"此主题：“{title}”已经存在了！"
        elif not title:
            error = "标题不能为空！"
        elif (
            startTime < planList_tmp.startTime.date()
            or deadLineTime > planList_tmp.deadLineTime.date()
        ):
            error = "计划的时间范围超过了计划列表的时间范围！"
        elif startTime > deadLineTime:
            error = "结束时间不能早于起始时间！"
        if error == None:
            try:
                plan = Plan(
                    id=plan_id,
                    title=title,
                    description=description,
                    startTime=startTime,
                    deadLineTime=deadLineTime,
                    createBy=createBy,
                    belongTo=belongTo,
                    completedStatus=plan_tmp.completedStatus,
                )
                db.session.delete(
                    Plan.query.filter_by(
                        id=plan_id, createBy=session.get("user_id")
                    ).first()
                )
                db.session.add(plan)
                db.session.commit()
            except Exception as e:
                error = f"计划：“{title}”修改失败。"
                db.session.rollback()
            else:
                flashDict["success"] = "修改计划成功"
        flashDict["error"] = error
        flash(flashDict)
    return redirect(url_for("plan.sel_plans", planList_id=planList_id))


@bp.route("/changeStatus/<int:planList_id>/<int:plan_id>", methods=["GET", "POST"])
@login_required
def change_status(planList_id, plan_id):
    '''
    更新Plan的状态为status参数的值
    1、已完成；0、未完成
    '''
    status = request.args.get("status", type=int)
    flashDict = {}
    try:
        plan_tmp = Plan.query.filter_by(
            id=plan_id, createBy=session.get("user_id")
        ).first()

        # 创建更新后的plan
        plan = Plan(
            id=plan_id,
            title=plan_tmp.title,
            description=plan_tmp.description,
            startTime=plan_tmp.startTime,
            deadLineTime=plan_tmp.deadLineTime,
            createBy=plan_tmp.createBy,
            belongTo=plan_tmp.belongTo,
            completedStatus=status,
        )
        db.session.delete(
            Plan.query.filter_by(id=plan_id, createBy=session.get("user_id")).first()
        )
        db.session.add(plan)
        db.session.commit()
    except Exception as e:
        error = f"计划：“{plan_tmp.title}”修改失败。"
        db.session.rollback()
    else:
        flashDict["success"] = "修改计划成功"

    # 重定向至plan的首页
    return redirect(url_for("plan.sel_plans", planList_id=planList_id))

from flask import Blueprint, render_template
from flask import flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, login_required
from jobplus.models import User, Company, Job


front = Blueprint('front', __name__)

@front.route('/')
def index():
    # 分别获取最新创建的12个公司信息和职位信息放到首页进行展示
    last12companies = Company.query.order_by(Company.created_tm.desc()).limit(12).all()
    last12jobs = Job.query.order_by(Job.created_tm.desc()).limit(12).all()

    return render_template('index.html', data=dict(job=last12jobs, company=last12companies))

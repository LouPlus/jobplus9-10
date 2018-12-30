from flask import Blueprint, render_template
from flask import flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, login_required
from jobplus.models import User, Company, Job
from jobplus.forms import LoginForm



front = Blueprint('front', __name__)

@front.route('/')
def index():
    # 分别获取最新创建的12个公司信息和职位信息放到首页进行展示
    last12companies = Company.query.order_by(Company.created_tm.desc()).limit(12).all()
    last12jobs = Job.query.order_by(Job.created_tm.desc()).limit(12).all()

    return render_template('index.html', data=dict(job=last12jobs, company=last12companies))
    return render_template('index.html')



@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_disable: #检查用户的状态是否为禁用,禁用状态不允许登录
            flash('用户已被禁用','danger')
            redirect(url_for('front.login'))
        else:
            login_user(user, form.remember_me.data)
            next_page = 'user.profile'
            if user.is_admin:
                next_page = 'admin.index'
            elif user.is_company:
                next_page = 'company.profile'
            return redirect(url_for(next_page))
    return render_template('login.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录', 'success')
    return redirect(url_for('.index'))

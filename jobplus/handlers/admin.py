from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request, current_app
from jobplus.models import db, User, Job
from flask_login import login_required, current_user
from jobplus.decorators import admin_required
from jobplus.forms import RegisterForm, UserProfileForm,CompanyProfileForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
	return render_template('admin/index.html', active='admin')

@admin.route('/users')
@admin_required
def users():
	page = request.args.get('page', default=1, type=int)
	pagination = User.query.paginate(
		page = page,
		per_page = current_app.config['ADMIN_PER_PAGE'],
		error_out = False
	)
	return render_template('admin/users.html', pagination=pagination)

@admin.route('/users/adduser', methods=['GET','POST'])
@admin_required
def adduser():
	form =  RegisterForm()
	if form.validate_on_submit():
		form.create_user() #默认创建普通求职者用户
		flash('求职者用户创建成功', 'success')
		return redirect(url_for('admin.users'))
	return render_template('admin/create_user.html', form=form)

@admin.route('/users/addcompany', methods=['GET','POST'])
@admin_required
def addcompany():
	form =  RegisterForm()
	if form.validate_on_submit():
		form.create_user(True) #企业用户创建时需要为role送入ROLE_COMPANY
		flash('企业用户创建成功', 'success')
		return redirect(url_for('admin.users'))
	return render_template('admin/create_company.html', form=form)

@admin.route('/users/<int:user_id>/edituser', methods=['GET','POST'])
@admin_required
def edituser(user_id):
	user = User.query.get_or_404(user_id)
	if not user.is_company:
		form =  UserProfileForm(obj=user)
	else:
		form =  CompanyProfileForm(obj=user.company)
	if form.validate_on_submit():
		form.update_profile(user)
		flash('更新信息成功', 'success')
		return redirect(url_for('admin.users'))
	return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/users/<int:user_id>/disable', methods=['GET','POST'])
@admin_required
def disableuser(user_id):
	user = User.query.get_or_404(user_id)
	if user.is_disable:
		user.is_disable = False
		flash('用户启用成功!','success')
	else:
		user.is_disable = True
		flash('用户已经禁用!','success')
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('admin.users'))


@admin.route('/jobs')
@admin_required
def jobs():
	page = request.args.get('page', default=1, type=int)
	pagination = Job.query.paginate(
		page = page,
		per_page = current_app.config['ADMIN_PER_PAGE'],
		error_out = False
	)
	return render_template('admin/jobs.html', pagination=pagination)


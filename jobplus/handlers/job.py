from flask import Blueprint, render_template, abort
from flask import flash, redirect, url_for, request, current_app
from jobplus.models import Job, Delivery, db
from flask_login import login_required, current_user
from jobplus.decorators import company_required
import re


job = Blueprint('job', __name__, url_prefix='/job')

@job.route('/')
def index():
	page = request.args.get('page', default=1, type=int)
	pagination = Job.query.order_by(Job.created_tm.desc()).paginate(
		page = page,
		per_page = current_app.config['COUNTS_PER_PAGE'],
		error_out = False
	)
	return render_template('job/index.html', pagination=pagination, active='job')

@job.route('/<int:job_id>')
def job_detail(job_id):
	job = Job.query.get_or_404(job_id)
	job.view_count += 1 #增加职位的浏览信息
	db.session.add(job)
	db.session.commit()
	return render_template('job/detail.html', job=job, active='')

@job.route('/<int:job_id>/apply')
@login_required
def delivery(job_id):
	job = Job.query.get_or_404(job_id)
	if job.current_user_is_deliveried:
		flash('该职位已投递!','warning')
	else:
		d = Delivery(
			job_id=job.id,
			user_id=current_user.id
		)
		db.session.add(d)
		db.session.commit()
		flash('投递成功', 'success')
	return redirect(url_for('job.job_detail', job_id=job.id))


@job.route('/<int:job_id>/enable')
@login_required
def enablejob(job_id):
	job = Job.query.get_or_404(job_id)
	if job.is_open:
		flash('该职位已上线!','warning')
	else:
		job.is_open = True
		db.session.add(job)
		db.session.commit()
		flash('该职位上线成功!','success')

        # 管理员和企业用户都可以上线下线职位,但是操作成功后返回的页面是不一样的
	if current_user.is_admin:
		return redirect(url_for('admin.jobs'))
	else:
		redirect(url_for('company.admin_index', company_id=job.company.id))


@job.route('/<int:job_id>/enable')
@login_required
def disablejob(job_id):
	pass

@job.route('/job/new')
@login_required
def addjob():
	pass

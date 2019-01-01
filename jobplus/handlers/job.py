from flask import Blueprint, render_template
from flask import flash, redirect, url_for, request, current_app
from jobplus.models import Job, Delivery, db
from flask_login import login_required, current_user
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

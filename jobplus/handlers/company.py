from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request, current_app
from jobplus.models import db, Company, Job, Delivery
from flask_login import login_required, current_user
from jobplus.forms import CompanyProfileForm, JobForm
from jobplus.decorators import company_required

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/')
def index():
	page = request.args.get('page', default=1, type=int)
	pagination = Company.query.order_by(Company.created_tm.desc()).paginate(
		page = page,
		per_page = current_app.config['COUNTS_PER_PAGE'],
		error_out = False
	)
	return render_template('company/index.html', pagination=pagination, active='company')

@company.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('你不是企业用户','warning')
        redirect(url_for('front.index'))
    form = CompanyProfileForm(obj=current_user.company)
    if form.validate_on_submit():
        form.update_profile(current_user) #企业信息配置表单里的更新函数送的是企业用户
        flash('企业信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)

@company.route('/<int:company_id>')
def company_detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/detail.html', company=company)

@company.route('/<int:company_id>/openjobs')
def company_openjobs(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/openjobs.html', company=company)


@company.route('/<int:company_id>/admin')
@company_required
def admin_index(company_id):
    company = Company.query.get_or_404(company_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(company_id=company_id).paginate(
        page = page,
        per_page = current_app.config['COUNTS_PER_PAGE'],
        error_out = False
    )
    #渲染模板时传入company参数要比company_id参数在模板使用方便些
    return render_template('company/admin_index.html', pagination=pagination, company=company)

@company.route('/<int:company_id>/admin/new', methods=['GET','POST'])
@company_required
def admin_addjob(company_id):
    company = Company.query.get_or_404(company_id)
    form = JobForm()
    if form.validate_on_submit():
        form.create_job(company)
        flash('职位发布成功!', 'success')
        return redirect(url_for('.admin_index', company_id=company.id))
    return render_template('company/admin_addjob.html', form=form, company=company)

@company.route('/<int:company_id>/admin/edit/<int:job_id>', methods=['GET','POST'])
@company_required
def admin_editjob(company_id,job_id):
    company = Company.query.get_or_404(company_id)
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位更新成功!', 'success')
        return redirect(url_for('.admin_index', company_id=company.id))
    return render_template('company/admin_editjob.html', form=form, company=company, job=job)

@company.route('/<int:company_id>/admin/delete/<int:job_id>')
@company_required
def admin_deljob(company_id,job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('职位信息删除成功', 'success')
    return redirect(url_for('.admin_index', company_id=company_id))

@company.route('/<int:company_id>/admin/apply/index')
@company_required
def admin_delivery_index(company_id):
    company = Company.query.get_or_404(company_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(company_id=company_id).order_by(Delivery.created_tm.desc()).paginate(
        page = page,
        per_page = current_app.config['COUNTS_PER_PAGE'],
        error_out = False
    )
    return render_template('company/admin_delivery_index.html', pagination=pagination, company=company)

@company.route('/<int:company_id>/admin/apply')
@company_required
def admin_delivery(company_id):
    company = Company.query.get_or_404(company_id)
    status = request.args.get('status')
    page = request.args.get('page', default=1, type=int)
    d = Delivery.query.filter_by(company_id=company_id)
    if status == 'checking':
        delivery_status = Delivery.STATUS_CHECKING
    elif status == 'accept':
        delivery_status = Delivery.STATUS_ACCEPT
    else:
        delivery_status = Delivery.STATUS_REFUSE
    d = d.filter(Delivery.status==delivery_status)
    pagination = d.order_by(Delivery.created_tm.desc()).paginate(
        page = page,
        per_page = current_app.config['COUNTS_PER_PAGE'],
        error_out = False
    )
    return render_template('company/admin_delivery.html', pagination=pagination, company=company, status=status)

@company.route('/<int:company_id>/admin/apply/<int:delivery_id>/accept')
@company_required
def admin_delivery_accept(company_id, delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    delivery.status = Delivery.STATUS_ACCEPT
    db.session.add(delivery)
    db.session.commit()
    flash('简历已审核,请联系面试', 'success')
    return redirect(url_for('company.admin_delivery', company_id=company_id))

@company.route('/<int:company_id>/admin/apply/<int:delivery_id>/refuse')
@company_required
def admin_delivery_refuse(company_id, delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    delivery.status = Delivery.STATUS_REFUSE
    db.session.add(delivery)
    db.session.commit()
    flash('简历已拒绝', 'success')
    return redirect(url_for('company.admin_delivery', company_id=company_id))

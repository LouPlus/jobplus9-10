from flask import Blueprint, render_template, flash, redirect, url_for
from jobplus.models import User
from flask_login import login_required, current_user
from jobplus.forms import CompanyProfileForm

company = Blueprint('company', __name__, url_prefix='/company')

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
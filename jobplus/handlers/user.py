from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from jobplus.models import User, Delivery
from flask_login import login_required, current_user
from jobplus.forms import UserProfileForm

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.update_profile(current_user)
        flash('个人信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html', form=form)


@user.route('/<int:user_id>')
@login_required
def person_page(user_id):
    user = User.query.get_or_404(user_id)
    deliverys = Delivery.query.filter_by(user_id=user_id).order_by(Delivery.created_tm.desc())
    return render_template('user/person_page.html', deliverys=deliverys, user=user)
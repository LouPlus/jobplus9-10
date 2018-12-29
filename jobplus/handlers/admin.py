from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request, current_app
from jobplus.models import Company
from flask_login import login_required, current_user
from jobplus.decorators import admin_required

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
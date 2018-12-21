from flask import Blueprint, render_template
from flask import flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, login_required
from jobplus.models import User, Company


front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')

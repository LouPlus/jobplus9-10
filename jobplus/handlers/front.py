from flask import Blueprint, render_template
from flask import flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, login_required


front = Blueprint('front', __name__)

@front.route('/')
def index():
    return 'hello jobplus9-10'

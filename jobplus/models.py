from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
from datetime import datetime


db = SQLAlchemy()

class Base(db.Model):
    """所有model的一个基类,默认添加了时间戳"""
    __abstract__ = True
    created_tm = db.Column(db.DateTime, default=datetime.utcnow)
    updated_tm = db.Column(db.DateTime, default=datetime.ttcnow, onupdate=datetime.utcnow)

""" 用户表与职位表多对多关系的中间表，用于用户和职位的关联，
	类似于实验楼第二周课程中创建sqlalchemy多对多关系里的course表和tag表多对多关联的course_tag中间表
"""
user_job = db.Table(
        'user_job',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
        db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE')),
        )

class User(Base, UserMixin):
	__tablename__ = 'user'

	ROLE_USER = 10
	ROLE_COMPANY = 20
	ROLE_ADMIN = 30

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True, nullable=False) #注册用户名
	realname = db.Column(db.String(64)) #简历上的名字
	email = db.Column(db.String(64), unique=True, index=True, nullable=False)
	_password = db.Column('password', db.String(256), nullable=False)
	role = db.Column(db.SmallInteger, default=ROLE_USER)
	mobilephone = db.Column(db.String(11))

	is_disable = db.Column(db.Boolean, default=False) #是否被禁用
	resume_url = db.Column(db.String(128)) #简历的地址
	jobs = db.relationship('job', secondary=user_job, backref='users') #与job建立关系


	def __repr__(self):
        return "<User:{}>".format(self.username)

	@property
	def password(self):
        return self._password

	@password.setter
	def password(self, orig_password):
        """自动为password生成哈希值存入_password"""
        self._password = generate_password_hash(orig_password)

	def check_password(self, password):
        """判断用户输入的密码和存储的hash密码是否相等"""
        return check_password_hash(self._password, password)

	@property
	def is_company(self):
		return self.role == ROLE_COMPANY

	@property 
	def is_admin(self):
		return self.role == ROLE_ADMIN

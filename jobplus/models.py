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
	updated_tm = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

	jobs = db.relationship('Job', secondary=user_job, backref=db.backref('users')) #与job建立关系

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

class Company(Base):
	__tablename__ = 'company'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), unique=True, index=True, nullable=False)
	logo = db.Column(db.String(512), nullable=False)
	site = db.Column(db.String(64), nullable=False)
	addr = db.Column(db.String(256), nullable=False) #地址
	email = db.Column(db.String(64), nullable=False)

	description = db.Column(db.String(1024)) #公司简介
	about = db.Column(db.String(8192)) #公司详情描述
	tags = db.Column(db.String(1024)) #公司标签,多个标签以逗号分割
	welfares = db.Column(db.String(1024))

	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
	user = db.relationship('User', uselist=False, backref=db.backref('company', uselist=False)) #uselist为False表示user和company是一对一的关系

	def __repr__(self):
		return '<Company:{}>'.format(self.name)


class Job(Base):
	__tablename__ = 'job'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(256)) #职位描述
	experience_requirement = db.Column(db.String(32)) #经验要求
	degree_requirement = db.Column(db.String(32)) #学历要求

	low_salary = db.Column(db.Integer, nullable=False)
	high_salary = db.Column(db.Integer, nullable=False)

	tags = db.Column(db.String(128), nullable=False) #职位标签,多个标签逗号分隔
	workplace = db.Column(db.String(32)) #工作地点
	view_count = db.Column(db.Integer, default=0) #查看次数

	is_open = db.Column(db.Boolean, default=True) #是否在招聘
	is_fulltime = db.Column(db.Boolean, default=True) #是否全职

	company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
	company = db.relationship('Company', uselist=False, backref=db.backref('job', cascade='all, delete-orphan'))

	def __repr__(self):
		return '<Job:{}>'.format(self.name)


class Delivery(Base):
	__tablename__ = 'delivery'


	STATUS_CHECKING = 1 #审核中
	STATUS_REFUSE = 2 #拒绝
	STATUS_ACCEPT = 3 #通过

	id = db.Column(db.Integer, primary_key=True)
	job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
	status = db.Column(db.SmallInteger, default=STATUS_CHECKING)

	response = db.Column(db.String(256)) #企业拒绝时的回复

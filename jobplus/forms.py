from flask_wtf import FlaskForm
from wtforms import ValidationError, TextAreaField, IntegerField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange, Regexp
from jobplus.models import db, User, Company, Job, Delivery


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('请输入用户名'), Length(3,64)])
    email = StringField('邮箱', validators=[DataRequired('请输入邮箱'), Email(message="邮箱格式不正确!")])
    password = PasswordField('密码', validators=[DataRequired('请输入密码'), Length(6,64)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired('请重复输入密码'), EqualTo('password', message='两次输入的密码不相同')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def create_user(self, is_company=False):
        if not is_company:
            user = User(username=self.username.data, email=self.email.data, password=self.password.data)
        else:
            user = User(username=self.username.data, email=self.email.data, password=self.password.data, role=User.ROLE_COMPANY)
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired('请输入邮箱'), Email(message='邮箱格式不正确!')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误,请重新输入')

class UserProfileForm(FlaskForm):
    realname = StringField('姓名',validators=[DataRequired('请输入简历上的真实姓名')])
    email = StringField('邮箱', validators=[DataRequired('请输入邮箱'), Email(message="邮箱格式不正确!")])
    password = PasswordField('密码(不填写保持不变)')
    mobilephone = StringField('手机号码', validators=[DataRequired('请输入手机号码'), Regexp('1[345789][0-9]{9}',message='手机号码格式不正确!')])
    work_years = IntegerField('工作年限', validators=[NumberRange(min=0, message='无效的工作年限')])
    resume_url = StringField('简历地址', validators=[URL(message='无效的URL地址')])
    submit = SubmitField('提交')

    def update_profile(self, user):
        user.realname = self.realname.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.mobilephone = self.mobilephone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        db.session.add(user)
        db.session.commit()


class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称')
    logo = StringField('Logo')
    site = StringField('公司网址', validators=[DataRequired(),URL(message='无效的URL地址')])
    addr = StringField('公司地址', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired('请输入邮箱'), Email(message='邮箱格式不正确!')])
    description = TextAreaField('公司简介') #公司简介
    about = TextAreaField('公司详情') #公司详情描述
    tags = StringField('公司标签,多个标签以逗号分割') #公司标签,多个标签以逗号分割
    welfares = TextAreaField('公司福利,多个标签以逗号分割')
    submit = SubmitField('提交')

    def update_profile(self, user):
        if user.company:
            company = user.company
        else:
            company = Company()
            company.user_id = user.id
        self.populate_obj(company)
        db.session.add(user)
        db.session.add(company)
        db.session.commit()

class JobForm(FlaskForm):
    name = StringField('职位名称',validators=[DataRequired()])
    low_salary = IntegerField('最低工资', validators=[DataRequired(), NumberRange(min=100, message='无效的最低工资')])
    high_salary = IntegerField('最高工资', validators=[DataRequired(), NumberRange(min=100, message='无效的最高工资')])
    workplace = StringField('工作地点',validators=[DataRequired()])
    tags = StringField('职位标签,多个标签以逗号分割',validators=[DataRequired()]) #公司标签,多个标签以逗号分割
    experience_requirement = SelectField('经验要求(年)',
        choices=[
        ('经验不限','经验不限'),('1年以上','1年以上'),('2年以上','2年以上'),('3年以上','3年以上'),('1到3年','1到3年'),('3到5年','3到5年'),('5年以上','5年以上')
        ])
    degree_requirement = SelectField('学历要求',
        choices=[('学历不限','学历不限'),('专科','专科以上'),('本科','本科以上'),('硕士','硕士以上'),('博士','博士'),]
        )
    description = TextAreaField('职位描述', validators=[Length(0,2018)])
    is_fulltime = BooleanField('是否全职')
    submit = SubmitField('发布')

    def create_job(self, company): #创建职位时需要传递公司信息
        job = Job()
        self.populate_obj(job)
        job.company_id = company.id
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self, job):
        self.populate_obj(job) #用传递进来的job信息填充表单进行展示
        db.session.add(job)
        db.session.commit()
        return job
        
class RefuseReason(FlaskForm):
    reason = StringField('拒绝原因',validators=[DataRequired(), Length(5,256)])
    submit = SubmitField('提交')

    def update(self, delivery):
        delivery.status = Delivery.STATUS_REFUSE
        delivery.response = self.reason.data
        db.session.add(delivery)
        db.session.commit()
        return delivery

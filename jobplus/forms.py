from flask_wtf import FlaskForm
from wtforms import ValidationError, TextAreaField, IntegerField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange, Regexp
from jobplus.models import db, User, Company

class RegisterForm(FlaskForm):
    pass


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
    resume_url = StringField('简历地址', validators=[URL('无效的URL地址')])
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
    site = StringField('公司网址', validators=[DataRequired(),URL('无效的URL地址')])
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
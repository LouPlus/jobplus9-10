import os
import json
from faker import Faker
from jobplus.models import db, User, Company, Job
from random import randrange

fake = Faker()
fake_cn = Faker('zh_CN') # 指定本地化区域参数,创建中文伪造数据,默认是英语


def iter_users():
    '''数据文件里爬取了33个公司的信息, 这里创建33个企业用户'''
    for i in range(33):
        email = fake_cn.email()
        user = User(
            username = fake.name(),
            realname = fake_cn.name(), 
            email = email,
            password = email, # 密码默认为邮箱
            role = User.ROLE_COMPANY,
            mobilephone = fake_cn.phone_number()
        )
        db.session.add(user)
        db.session.commit()

def iter_companies():
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'companies.json')) as f:
        companies = json.load(f)

    for i, company in enumerate(companies):
        user = User.query.get(i+1) #一个企业用户对应一个企业信息
        company = Company(
            name = company['name'],
            logo = company['logo'],
            site = fake_cn.url(),
            addr = company['addr'],
            email = fake_cn.email(),
            description = company['description'],
            about = company['about'],
            tags = company['tags'],
            welfares = company['welfares'],
        )
        company.user_id = user.id
        company.user = user
        db.session.add(company)
        db.session.commit()
def iter_jobs():
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'jobs.json')) as f:
        jobs = json.load(f)

    for i, job in enumerate(jobs):
        index = (i%33)+1
        company = Company.query.get(index)
        job = Job(
            name = job['name'],
            description = job['description'], #职位描述
            experience_requirement = job['experience_requirement'], #经验要求
            degree_requirement = job['degree_requirement'], #学历要求
            low_salary = randrange(5000,8000,1000),
            high_salary = randrange(8000,20000,1000),
            tags = ''.join([fake_cn.word() for i in range(3)]), #职位标签,多个标签逗号分隔
            workplace = job['workplace'], #工作地点
            company_id = company.id,
            company = company
            )
        db.session.add(job)
        db.session.commit()


def run():
    iter_users()
    iter_companies()
    iter_jobs()
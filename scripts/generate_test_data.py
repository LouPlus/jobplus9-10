import os
import json
from faker import Faker
from jobplus.models import db, User, Company

fake = Faker()
fake_cn = Faker('zh_CN') # 指定本地化区域参数,创建中文伪造数据,默认是英语


def iter_users():
    '''数据文件里爬取了13个公司的信息, 这里创建13个企业用户'''
    for i in range(13):
        email = fake_cn.email()
        yield User(
            username = fake.name(),
            realname = fake_cn.name(), 
            email = email,
            password = email, # 密码默认为邮箱
            role = User.ROLE_COMPANY,
            mobilephone = fake_cn.phone_number()
        )

def iter_companies():
    with open(os.path.join(os.path.dirname(__file__), '..', 'datas', 'companies.json')) as f:
        companies = json.load(f)

    for i, company in enumerate(companies):
        user = User.query.get(i+1) #一个企业用户对应一个企业信息
        yield Company(
            name = company['name'],
            logo = company['logo'],
            site = fake_cn.url(),
            addr = company['addr'],
            email = fake_cn.email(),
            description = company['description'],
            about = company['about'],
            tags = company['tags'],
            welfares = company['welfares'],
            user = user
        )


def run():
    for user in iter_users():
        db.session.add(user)

    for company in iter_companies():
        db.session.add(company)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
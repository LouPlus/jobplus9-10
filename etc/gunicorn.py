import multiprocessing

bind = '127.0.0.1:8000'

# ���鷨��-gunicorn��worker����Ϊcpu�˵ĸ�����2����1
workers = multiprocessing.cpu_count() * 2 + 1

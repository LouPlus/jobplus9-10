import multiprocessing

bind = '127.0.0.1:8000'

# 经验法则-gunicorn的worker数量为cpu核的个数的2倍加1
workers = multiprocessing.cpu_count() * 2 + 1

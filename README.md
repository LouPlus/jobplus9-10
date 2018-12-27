# jobplus9-10

### 组员 
* [leeboyjcc](https://github.com/leeboyjcc)
* [louix](https://github.com/louixid)
* [KRzhao](https://github.com/Nuonzhao)
* [郭靖_](https://github.com/174987598)
* [萧丰林](https://github.com/ethansiew)


### python version
* 实验楼Python3 具体是3.5.3


### steps for run project [shiyanlou environment]
* 修改MySQL字符编码设置为utf8<br>
   [client] default-character-set = utf8<br>
   [mysqld] character-set-server = utf8<br>
   [mysql] default-character-set = utf8<br>
  
 * 安装Python3 虚拟环境<br>
  virtualenv -p /usr/bin/python3 env<br>
  source env/bin/activate<br>
  pip install -r requirements.txt [install required packages]<br>
  deactivate [Python虚拟环境安装好packages以后，需要重新激活才能使用]<br>
  source env/bin/activate<br>
 
 * mysql<br>
  sudo service mysql start<br>
  mysql -uroot<br>
  create database jobplus<br>
  
 * create tables<br>
  flask db init<br>
  flask db migrate -m "init database"<br>
  flask db upgrade<br>
  
 * 生成测试数据<br>
  export FLASK_APP=manage.py<br>
  export FLASK_DEBUG=1<br>
  flask shell<br>
  from scripts.generate_test_data import run<br>
  run()<br>
 
 * run<br>
  flask run<br>
  


# 我们需要的服务有

# MySQL：数据库服务
# Nginx：高性能Web服务器+负责反向代理；
# Supervisor：监控服务进程的工具；
# gunicorn:

# [Flask与WSGI](https://www.cnblogs.com/rgcLOVEyaya/p/RGC_LOVE_YAYA_830days_1.html)
# [WSGI及flask web框架启动](https://blog.csdn.net/m0_37519490/article/details/80704717)
# 首先理解 nginx gunicorn wsgi supervisor 到底有什么作用
#
# 一个请求的具体过程:
#
#         前端文件直接反向代理
#               ^                      通过WSGI协议交互, 把request发送给application
#               |                                                           |
# request --> Nginx 服务器 --> HTTP协议请求 --> WSGI 服务器 --> WSGI application(flask)
#
#
# WSGI 服务器(如 Gunicorn，uWSGI):
# WSGI(Web Server Gateway Interface)是WEB服务器和web框架或web应用之间建立的一种简单通用的接口规范
# 根据web服务器传递而来的参数构建一个让WSGI应用成功执行的环境，例如request,
# 将request发送给WSGI application, 还得把应用处理好的请求返回给web服务器
#
# 一般应用服务器(例如flask 的 app.run)都集成了web服务器，主要是为了调试方便，
# 出于性能和稳定性考虑，并不能在生产环境中使用。
#
#
# WSGI application: 接收request, 返回 response 给 WSGI server

# Web服务器(HTTP 服务器): 例如 Nginx. 当Web浏览器(客户端)连到服务器上并请求文件时，
# 服务器将处理该请求并将文件发送到该浏览器上，附带的信息会告诉浏览器如何查看该文件（即文件类型）
# 服务器使用HTTP（超文本传输协议）进行信息交流，这就是人们常把它们称为HTTP服务器的原因。
# 严格意义上Web服务器只负责处理HTTP协议，用于处理静态页面的内容。而动态内容需要通过WSGI接口交给应用服务器去处理。

# Nginx作用:
# 负载均衡: 在实际应用中我们通常会让Nginx监听（绑定）80端口，通过多域名或者多个location分发到不同的后端应用。
# 拦截静态请求，Nginx会拦截到静态请求（静态文件，如图片），并交给自己处理。而动态请求内容将会通过WSGI容器交给Web应用处理;
# ...

# 首先,要有如下的文件

# 1. wsgi 文件
# 2. config.py 分为应用的本地配置和服务器配置
# 3. supervisor 的配置
# 4. nginx 的配置


# 将项目文件上传到 github

# 在服务器上克隆项目
"""
git clone https: // github.com/xuxmin/Book_Manage_System.git
"""

# 将项目所需要的各种服务安装好

# 初始化数据库
"""
mysql -u root -p < schema.sql
"""

# 修改一下服务器的配置文件 config.py
# 记住调整成生产模式, 而不是开发模式


# 可以先尝试运行一下项目, 使用flask自带的最简单的app.run, 能运行成功就行
"""
python3 app.py
"""

# 虽然像上面这样能够运行成功, 但是实际中并不能这么做
# 1. 如果关闭了程序, 别人就访问不了了
# 2. 性能太差

# 所以我们使用一个 gunicorn WSGI容器来运行web应用

# 先准备一个 wsgi 文件
"""
import sys
from os.path import abspath
from os.path import dirname

# 设置当前目录为工作目录
sys.path.insert(0, abspath(dirname(__file__)))

# 引入 app.py
import app

# 将 flask 的实例赋值给 application 变量
# 必须要有 application 这个变量, 是给 gunicorn 用的
# WSGI协议规定
application = app.app
"""

# 使用 WSGI容器 运行web服务, 这里是gunicorn 有些博客用的是 uWSGI
# 启动 gunicorn
# $ gunicorn [options] module_name:variable_name
# module_name对应python文件，variable_name对应web应用实例
# 我们在上面将module_name:variable_name 写在了 wsgi.py 文件中
# 所以用下面的方法
"""
# 启动 gunicorn
➜  Book_Manage_System git:(master) ✗ gunicorn wsgi --bind 0.0.0.0:4000
[2019-04-22 10:34:30 +0800] [28117] [INFO] Starting gunicorn 19.9.0
[2019-04-22 10:34:30 +0800] [28117] [INFO] Listening at: http://0.0.0.0:4000 (28117)
[2019-04-22 10:34:30 +0800] [28117] [INFO] Using worker: sync
[2019-04-22 10:34:30 +0800] [28120] [INFO] Booting worker with pid: 28120
"""
# wsgi 是前面写的那个文件, 提供 application
# 0.0.0.0 表示所有 ip 地址都能访问
# 4000 表示端口

# 我们使用了 gunicorn 这个后, 还想让web应用能够开机自动运行
# 挂了也自动运行, 关机仍在运行, 这就需要一个额外的监护程序 supervisor
# 安装好后在/etc/会生成一个supervisord.conf文件及一个supervisord.d文件目录
# supervisord.conf是一些默认配置，可自行修改：
# supervisord.d目录用来存放用户自定义的进程配置

# 我们想要在 /etc/supervisor/conf.d/ 目录下写一个文件 bms.conf 表示这个进程的配置
# 下面是 bms.conf 文件的内容(后缀必须为.conf)
"""
[program:bms]
command=/usr/local/bin/gunicorn wsgi --bind 0.0.0.0:4000 --pid /tmp/bms.pid
directory=/root/Book_Manage_System
autostart=true
autorestart=true
"""
# 配置写在本地，然后在服务器上建一个链接
# 建立一个软连接  ln -s /root/Book_Manage_System/bms.conf /etc/supervisor/conf.d/bms.conf   全称
# 还可以将建立软连接的代码写成脚本

# 使用下面的命令重启 supervisor 即可
"""
service supervisor restart
"""
# supervisor 其他命令
"""
supervisorctl stop xxx          # 停止某一个进程(xxx)
supervisorctl status            # 查看当前运行的进程列表
supervisorctl start xxx         # 启动某个进程
supervisorctl restart xxx       # 重启某个进程
"""

# 接下来配置 Nginx
# bms.nginx 应该放在 /etc/nginx/sites-enabled/ 下
"""
server {
    listen 80;
    location / {
        proxy_pass http://localhost:4000;
    }
}
"""
# 建立软连接
"""
ln -s /root/Book_Manage_System/bms.nginx /etc/nginx/sites-enabled/bms
"""
# 使用 ll 或者 cat 一下来判断是否成功建立链接

# 最后重启 nginx
"""
service nginx restart
"""

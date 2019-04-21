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

# wsgi 文件
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
gunicorn wsgi --bind 0.0.0.0:3000 --pid /tmp/blog.pid
"""


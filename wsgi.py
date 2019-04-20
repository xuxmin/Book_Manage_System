#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

# 设置当前目录为工作目录
sys.path.insert(0, abspath(dirname(__file__)))

# 引入 app.py
import app

# 必须有一个叫做 application 的变量
# gunicorn 就要这个变量
# 这个变量的值必须是 Flask 实例
# 这是规定的套路(协议)
application = app.app

# 这是把代码部署到 apache gunicorn nginx 后面的套路
# 上面是 wsgi 的配置

# 下面的方式也不想？？？
# gunicorn wsgi --bind 0.0.0.0:2000

# 我们想开机自动运行？


# 一个supervisor，监护程序，可以自动重启等等
# 下面是 supervisor 的配置， 我们已经将其写入了配置文件，并设置为软连接到 指定目录
"""
➜  ~ cat /etc/supervisor/conf.d/blog.conf

在 xx.conf 中写入如下代码

[program:blog]
command=/usr/local/bin/gunicorn wsgi --bind 0.0.0.0:2000 --pid /tmp/blog.pid
directory=/root/Blog
autostart=true
autorestart=true

supervisorctl restart todo
service supervisor restart
"""

# 使用下面的方式启动程序
"""
启动程序命令
gunicorn wsgi --bind 0.0.0.0:3000 --pid /tmp/blog.pid

不对，如果程序对的话，直接 service supervisor restart 就行了，不用专门输入上面的命令

如果程序有问题，可以用上面的命令启动，然后测试
"""


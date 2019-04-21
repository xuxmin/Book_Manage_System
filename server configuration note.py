
# 首先,要有如下的文件

# 1. wsgi 文件
# 代码如下
"""
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
"""
# 2. config.py 分为应用的本地配置和服务器配置

# 3. supervisor 的配置

# 4. nginx 的配置


# 我们需要的服务有
# Nginx：高性能Web服务器+负责反向代理；
# Supervisor：监控服务进程的工具；
# MySQL：数据库服务。
# 


# 将项目文件上传到 github

# 在服务器上克隆项目
"""
git clone https: // github.com/xuxmin/Book_Manage_System.git
"""

# 初始化数据库
"""
mysql -u root -p < schema.sql
"""

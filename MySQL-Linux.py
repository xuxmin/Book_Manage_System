
# 参考 https://www.cnblogs.com/zhanggl/p/3985678.html

# 安装 MySQL 
"""
sudo apt-get install mysql-server
"""
# 安装完成后，MySQL服务器会自动启动，我们检查MySQL服务器程序
# ps -aux|grep mysql
"""
➜  / ps -ax|grep mysql
26343 ?        Sl     0:00 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid
26444 pts/0    S+     0:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn mysql
"""

# 检查MySQL服务器占用端口
"""
➜  / netstat -nlt|grep 3306
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN
"""

# 通过系统服务命令检查MySQL服务器状态
"""
➜  / service mysql status
● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2019-04-21 21:42:20 CST; 5min ago
 Main PID: 26343 (mysqld)
    Tasks: 27 (limit: 2325)
   CGroup: /system.slice/mysql.service
           └─26343 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid

Apr 21 21:42:20 iZuf6hw1svmpux3orznc1aZ systemd[1]: Starting MySQL Community Server...
Apr 21 21:42:20 iZuf6hw1svmpux3orznc1aZ systemd[1]: Started MySQL Community Server.
"""

# 安装MySQL服务器，会自动地一起安装MySQL命令行客户端程序。
# 在本机输入mysql命令就可以启动，客户端程序访问MySQL服务器。
"""
➜  / mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.25-0ubuntu0.18.04.2 (Ubuntu)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
"""

# 新建用户guest, 授权bms数据库的所有权限, 可在任何网段访问， 用户名为guest，密码为guest19981028
"""
GRANT ALL ON bms.* to guest@'%' IDENTIFIED BY 'guest19981028';
"""


# 安装 mysql-connector
"""
 pip3 install mysql-connector
"""

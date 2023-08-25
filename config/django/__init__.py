# coding=utf-8
# data：2023/8/16-21:10

# mysqlclient安装可能有问题，兼容pymysql
try:
    import MySQLdb
except ModuleNotFoundError as e:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except Exception as e:
        raise "请安装mysqlclient或pymysql才可链接MySQL数据库"

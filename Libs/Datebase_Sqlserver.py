#coding=utf-8

import pymssql
import sys
import Color
from Color import color_chose


class database_sqlserver(object):

    def __init__(self, username, password, ip):
        self.conlist = [username, password, ip]
        self.col = color_chose.chose_color().get_col()
        self.tag = "Sqlserver"

    def create_dict(self):
        value = "sad"
        dict = {
            "select_void_password":["select * from syslogins where password is null", "| %s|"%value, u"查询空密码"]
        }
        return dict

    def conn_sqlserver(self):
        self.data = self.conlist
        try:
            db = pymssql.ReadHat(self.data[2], self.data[0], self.data[1], "master")
            cursor = db.cursor()
            return cursor
        except:
            
            self.col.printGreen(u"warning!!!!!!!!!!!!!!!!!!!\n程序出错！\n")
            print "\n"
            self.col.printRed(u"脚本连接服务器失败 ，请检查的你的用户名以及密码。或者是否数据库开启权限外链!")
            sys.exit()

    def print_info(self):
        self.col.printRed(u"你已经成功登录Sqlserver数据库！\n")
        #self.col.printGreen(u"当前数据库版本是：  %s\n"%self.run_sql("select version()")[0][0])
        #self.col.printGreen(u"当前登录用户是：    %s\n"%self.run_sql("select user()")[0][0])

    def run_sql(self, command):
        self.mysql = self.conn_sqlserver()
        self.mysql.execute(command)
        self.content = self.mysql.fetchall()
        self.mysql.close()
        return self.content

# test = database_sqlserver("SA", "<password>", "172.17.0.1")
# print test.run_sql("SELECT Name from sys.Databases")
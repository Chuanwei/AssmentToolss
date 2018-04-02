#coding=utf-8

import sys
import Color
import DB
import tqdm
from Color import color_chose
import pymysql
import time
from DB import mysql_Level2
from tqdm import tqdm,trange

class Database(object):

    def __init__(self, username="", password="", ip="", port=""):
        self.conn_list = [username, password, ip, int(port)]
        self.col = color_chose.chose_color().get_col()
        # self.cursorclass = MySQLdb.cursors.DictCursor
        self.tag = "mysql"
        self.savename = self.conn_list[2] +"-"+ self.tag +"-"+ time.strftime('%Y-%m-%d',time.localtime(time.time()))


    def create_dict(self):
        """
        :return dict
        """
        lis = ["host", "user", "password"]
        lis1 = ["Variable_name", "Value"]
        lis2 = ["Grants for root@localhost"]
        newdict = [
            "select host,user,authentication_string from mysql.user;",
            "show global variables like '%max_connect%';",
            "show variables like '%skip_networking%';",
            "show grants for root@'localhost';",
            "select host,user,authentication_string from mysql.user;",
            "select host,user,authentication_string from mysql.user;",
            "show variables like '%log%';",
            "select version();",
            "select host,user,authentication_string from mysql.user;"
        ]
        if self.run_sql("select version()")[0][0] >= "5.7":
            pass
        else:
            newdict[0] = "select host,user,password from mysql.user;"
            newdict[4] = "select host,user,password from mysql.user;"
            newdict[5] = "select host,user,password from mysql.user;"
            newdict[8] = "select host,user,password from mysql.user;"
        return newdict
    def print_info(self):
        self.col.printRed(u"你已经成功登录mysql数据库！\n")
        self.col.printGreen(u"当前数据库版本是：  %s\n"%self.run_sql("select version()")[0][0])
        self.col.printGreen(u"当前登录用户是：    %s\n"%self.run_sql("select user()")[0][0])

    def conn_mysql(self):
        self.data = self.conn_list
        try:
            db = pymysql.connect(host = self.data[2], user = self.data[0], passwd = self.data[1], port = self.data[3])
            cursor = db.cursor()
            return cursor
        except Exception as e:
            self.col.printRed(e[1] + "\n")
            if e[0] == 1045:
                self.col.printRed(u"用户名或密码错误!\n请检查你的用户名和密码是否正确！\n")
                sys.exit()
            elif e[0] == 2003:
                self.col.printRed(u"无法连接对方mysql服务!\n请检测你是否可以连接到对方网络,ip端口是否输入正确, 或者对方数据库不支持外链!\n")
                sys.exit()
            else:
                self.col.printBlue(u"未知错误！\n")
                sys.exit()

    def run_sql(self, command):
        try:
            self.mysql = self.conn_mysql()
            self.mysql.execute(command)
            self.content = self.mysql.fetchall()
            self.mysql.close()
            return self.content
        except:
            return ""

    def create_excel_data(self):
        dict = self.create_dict()
        result = {}
        for d in tqdm(range(0, len(dict))):
            time.sleep(1)
            if d == 0:
                result["D%s"%(d+2)] = mysql_Level2.check_uservoid([self.run_sql(dict[d]), dict[d]])
            elif d == 1:
                result["D%s" % (d + 2)] = mysql_Level2.check_terminal_ReadHat([self.run_sql(dict[d]), dict[d]])
            elif d == 2:
                result["D%s" % (d + 2)] = mysql_Level2.check_skip([self.run_sql(dict[d]), dict[d]])
            elif d == 3:
                result["D%s" % (d + 2)] = mysql_Level2.check_userRights(self.grate_result())
            elif d == 4:
                result["D%s" % (d + 2)] = mysql_Level2.check_terminal_ReadHat([self.run_sql(dict[d]), dict[d]])
            elif d == 5:
                result["D%s" % (d + 2)] = mysql_Level2.check_uservoid([self.run_sql(dict[d]), dict[d]])
            elif d == 6:
                result["D%s" % (d + 2)] = mysql_Level2.check_audit([self.run_sql(dict[d]), dict[d]])
            elif d == 7:
                result["D%s" % (d + 2)] = mysql_Level2.check_version([self.run_sql(dict[d]), dict[d]])
            elif d == 8:
                result["D%s" % (d + 2)] = mysql_Level2.check_terminal_setting([self.run_sql(dict[d]), dict[d]])
        return result

    def grate_result(self):
        self.userlist = ["show grants for {};".format(i[0].split(":")[1][1:-1]) for i in self.run_sql(
            "SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS query FROM mysql.user;")]
        sqlresult = []
        for i in self.userlist:
            sqlresult.append(self.run_sql(i))
        return [sqlresult, self.userlist]

    def check_statue(self):
        """
        ＠函数方法:检测数据库类是是否正常运行
        :return: 
        """
        self.data = self.conn_list
        try:
            db = pymysql.connect(host = self.data[2], user = self.data[0], passwd = self.data[1], port = self.data[3])
            return (10086, 'access')
        except Exception as e:
            if e[0] == 1045:
                content = u"用户名或密码错误!\n请检查你的用户名和密码是否正确！\n"
                return (e[0], content)
            elif e[0] == 2003:
                content = u"无法连接对方mysql服务!\n请检测你是否可以连接到对方网络,ip端口是否输入正确, 或者对方数据库不支持外链!\n"
                return (e[0], content)
            else:
                err = 5800
                content = u"未知错误！\n"
                return (err, content)




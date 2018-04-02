#encoding=utf-8
import Color
import excel
import _mssql
import sys
from Color import OS_Check
from excel.Excel import *
class Master():

    def __init__(self):
        self.request = ""
        self.conn = {
            "host":"",
            "username":"",
            "password":"",
            "port":"",
            "xe":"XE",
        }
        self.hash = ""
        self.col = OS_Check.OS().get_col()
        self.DB_hash = ["a189c633d9995e11bf8607170ec9a4b8", "81c3b080dad537de7e10e0987a4bf52e", "0c0134c0cbebf48be8c95920f5ea74fc"]
        self.OS_hash = ["3d6a48f6562b53e3c55c010518d9cf9c"]

    def check_option(self):
        """
        @函数功能:检查是否可以连通目标状态
        :return: 
        """
        p = 0
        for i in self.conn:
            if self.conn[i] != "":
                p += 1
        return p

    def run(self, value):
        num = self.check_option()
        if value == "run":
            # print len([i for i in self.conn])
            if num >= 4:
                db = OS_Check.OS().get_database_conn(self.hash, self.conn)
                print db.check_statue()
                try:
                    value = db.check_statue()
                    if value[0] == 10086:
                        self.col.printBlue(u"连接成功，运行中!!!!!!!\n")
                        excel = Excel_Create(db.tag, db.savename)
                        # os = Linux_readhat.ReadHat("127.0.0.1", 22, "lioder", "ddss223336411")
                        # aa = Excel_Create(os.tag, os.savename)
                        # print os.savename
                        # aa.result_introduction(row=[2, 0], celdata=os.create_excel_data())
                        try:
                            excel.result_introduction(row=[2, 0], celdata=db.create_excel_data())
                            self.col.printBlue(u"生成文件成功！文件路径为： %s \n" % excel.savename)
                        except Exception as e:
                            self.col.printRed(u"生成文件失败， 错误原因： %s \n" % e)

                    elif value[0] == 1045:
                        self.col.printRed(value[1])
                    elif value[0] == 2003:
                        self.col.printRed(value[1])
                except Exception as e:
                    print db.check_statue()
                    print e



            else:
                self.col.printBlue(u"你需要设置完以下参数！(oracle所需要的实例-------------)")
                self.option("option")

    def option(self,value):
        try:
            if value == "option":
                str = u"""
    host            username            password            port        xe
    %-16s%-20s%-20s%-15s%s
    你需要设置完参数才能扫描!    (oracle所需要的实例-------------)
    """%(self.conn["host"], self.conn["username"], self.conn["password"], self.conn["port"], self.conn["xe"])
                self.col.printBlue(str)
        except KeyError:
            self.col.printRed(u"你需要设置完参数才能扫描(oracle所需要的实例-------------) \n")
            str = u"""
host            username            password            port

你需要设置完参数才能扫描!(oracle所需要的实例-------------)
"""
            self.col.printBlue(str)
    def set(self, value):
        """
        set 命令
        :param value: 
        :return: conn 字典
        """
        if value[:3] == "set":
            if value.split(" ")[1] == "username":
                self.conn["username"] = value.split(" ")[2]
            elif value.split(" ")[1] == "password":
                self.conn["password"] = value.split(" ")[2]
            elif value.split(" ")[1] == "host":
                self.conn["host"] = str(value.split(" ")[2])
            elif value.split(" ")[1] == "port":
                self.conn["port"] = int(value.split(" ")[2])
            elif value.split(" ")[1] == "xe":
                self.conn["xe"] = value.split(" ")[2]
        return self.conn

    def exit(self, value):
        """
        退出命令
        :param value: 
        :return: 
        """
        if value == "exit":
            sys.exit()
    def use(self, value):
        str1 = u"""
你可以选择一个数据库类型进行扫描
load 10 or load 11

ID      数据库类型
10      mysql
11      oracle
"""
        str2 = u"""
你可以选择load 13
ID      主机类型
13      RedHat

"""

        if value[:3] == "use":
            if value[4:] == "1":
                self.col.printRed(str1)
                self.request = "数据库扫描"
                return True
            elif value[4:] == "2":
                self.col.printRed(str2)
                self.request = "主机扫描"
                return True
            else:
                self.col.printRed(u"请选择正确的扫描ＩＤ!\n")
                return False
        else:
            return False

    def back_1(self, value):
        if value == "back":
            text = \
u"""
%s         %s
 1         数据库扫描                  
 2         主机扫描
 3         网络路由扫描
 4         windows规则文件读取

""" % ("ID", u"功能")
            self.col.printRed(text)
            self.request = ""
            self.shell_()
            self.start()

    def back_2(self, value):
        if value == "back":
            useexample = u"""
你需要设置扫描的信息
example:
set username root
set password root
set port 3306/1521
set host 192.168.0.6
数据库扫描$:run 

"""
            if self.request.split("/")[1] in ("oracle", "mysql"):
                self.request = "数据库扫描"
            else:
                self.request = "主机扫描"
            while 1 :
                value = self.shell_()
                self.exit(value)
                self.back_1(value)
                self.load(value)
                if self.hash != "":
                    self.col.printRed(useexample)
                    self.exit(value)
                    while 1:
                        value = self.shell_()
                        self.exit(value)
                        self.set(value)
                        self.option(value)
                        self.run(value)




    def start(self):
        title = "%-11s%-20s" % (u"ID", u"功能")
        text = \
u"""
%s
 1         数据库扫描                  
 2         主机扫描
 3         网络路由扫描
 4         windows规则文件读取

""" % title
        self.col.printRed(text)
        while 1:
            value = self.shell_()
            self.exit(value)
            if self.use(value) == False:
                self.col.printRed(u"%s 命令未找到" % value)
            else:
                self.run_conn()



    def load(self, value):
        if value[:4] == "load":
            if value[5:] == "10":
                self.request = "数据库/mysql"
                self.hash = "81c3b080dad537de7e10e0987a4bf52e" #mysql hash
            elif value[5:] == "11":
                self.request = "数据库/oracle"
                self.hash = "a189c633d9995e11bf8607170ec9a4b8"
            elif value[5:] == "13":
                self.request = "主机/Redhat"
                self.hash = "e2798af12a7a0f4f70b4d69efbc25f4d"

    def shell_(self,):
        """
        终端显示
        :param value: 
        :返回输入的参数 
        """
        str = self.request + "$:"
        return self.col.inputGreen(u"%s"%str)

    def back(self, value):
        if value == "back":
            while 1:
                pass



    def get_IO(self):
        welcome = \
        u"""
 _____    _____    _____   _____  
|_   _|  / ____|  / ____| |  __ \ 
  | |   | |      | (___   | |__) |
  | |   | |       \___ \  |  ___/ 
 _| |_  | |____   ____) | | |     
|_____|  \_____| |_____/  |_|   



        \n"""
        self.col.printGreen(welcome)
        test = u"欢迎使用，请选择你的使用库／（ㄒｏㄒ）／～～"
        self.col.printRed(test)
        title = "%-11s%-20s"%(u"ID", u"功能")
        text = \
u"""
%s
 1         数据库扫描                  
 2         主机扫描

"""%title
        self.col.printRed(text)
        while 1:
            value = self.shell_()
            self.exit(value)
            if self.use(value) == False:
                self.col.printRed(u"%s 命令未找到"%value)
            else:
                self.run_conn()



    def run_conn(self):
        useexample = u"""
你需要设置扫描的信息
example:
set username root
set password root
set port 3306/1521
set host 192.168.0.6
数据库扫描$:run 

"""
        while 1:
            value = self.shell_()
            self.exit(value)
            self.back_1(value)
            self.load(value)
            if self.hash != "":
                self.col.printRed(useexample)
                self.exit(value)
                while 1:
                    value = self.shell_()
                    self.back_2(value)
                    self.exit(value)
                    self.set(value)
                    self.option(value)
                    self.run(value)

if __name__ == "__main__":

    a = Master()
    a.get_IO()






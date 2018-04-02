#coding=utf-8

import cx_Oracle
import sys,os
import Color
import DB
import tqdm
from Color import color_chose
from DB import oracle_Level2
import time
from tqdm import tqdm,trange

class database_oracle(object):

    def __init__(self, username, password, ip, port, xe = ""):
        self.conlist = [username, password, ip, port]
        self.col = color_chose.chose_color().get_col()
        self.oracle_server = self.conlist[2] + "/DB"
        self.tag = "Oracle"
        self.savename = self.conlist[2] + "-" + self.tag + "-" + time.strftime('%Y-%m-%d',
                                                                                 time.localtime(time.time()))
        if xe == "":
            self.xe = "XE"
        else:
            self.xe = xe


    def create_dict(self):
        """
        @函数功能:返回一个和ｅｘｃｅｌ表顺序的ｓｑｌ语句执行结果
        :return: 
        """
        excel_sql = [
            "select limit from dba_profiles s where s.profile = 'DEFAULT' and s.resource_name in ('PASSWORD_LIFE_TIME', 'PASSWORD_VERIFY_FUNCTION')",
            "select resource_name, limit from dba_profiles s where s.profile='DEFAULT' and s.resource_name in ('FAILED_LOGIN_ATTEMPTS', 'PASSWORD_LOCK_TIME')",
            "select name,value from v$parameter where name='remote_os_authent'",
            "",
            "select username from dba_users_with_defpwd s where s.username in (select username from dba_users s where s.account_status = 'OPEN')",
            "select username from dba_users s where s.account_status = 'OPEN'",
            "select parameter,value from v$option where parameter = 'Oracle Label Security'",
            "select value from v$parameter where name = 'audit_trail'",
            "",
            "",
            "select value from v$option where parameter = 'Oracle Database Vault'",
            "select * from v$version"
        ]
        return excel_sql


    def conn_oracle(self):
        self.data = self.conlist
        try:
            tns_name = cx_Oracle.makedsn(self.conlist[2], self.conlist[3], "%s"%self.xe)
            db = cx_Oracle.connect(self.conlist[0],self.conlist[1], tns_name)
            return db
        except:
            self.col.printGreen(u"warning!!!!!!!!!!!!!!!!!!!\n程序出错！\n")
            print "\n"
            self.col.printRed(u"脚本连接服务器失败 ，请检查的你的用户名以及密码。或者是否数据库开启权限外链!")
            sys.exit()

    def print_info(self):
        self.conn_oracle()
        self.col.printRed(u"你已经成功登录Oracle数据库！\n")
        self.col.printGreen(u"当前数据库版本为：  %s\n"%self.conn_oracle().version)
        self.col.printGreen(u"当前连接信息为：    %s\n"%self.conn_oracle().dsn)
        self.col.printGreen(u"已找到当前Oracle数据库目录：%s\n"%self.getpath()[0])
        self.buding_echo()

    def get_grantee(self):
        """
        把用户权限分配为特定结果
        @:return result用于oracle check函数
        """
        sql = [
            "select grantee,granted_role from dba_role_privs s where s.grantee in (select username from dba_users s where s.username not in ('SYS', 'SYSTEM') AND s.account_status = 'OPEN')",
            "select grantee,privilege from dba_sys_privs s where s.grantee in (select username from dba_users s where s.username not in ('SYS', 'SYSTEM') AND s.account_status = 'OPEN')",
            "select grantee,table_name,privilege from dba_tab_privs s where s.grantee in (select username from dba_users s where s.username not in ('SYS', 'SYSTEM') AND s.account_status = 'OPEN')",
        ]
        result = map(lambda x:self.run_sql(x), sql)
        return [result, sql]

    def getpath(self):
        ser_path = self.run_sql("select name,value from v$parameter where name like '%spfile%'")[0][1][:-21]
        str = ser_path[2]
        new_path = ser_path.replace(str, "//")
        SQLNET_ORA = new_path + "//network/admin/sqlnet.ora"
        self.check_file("utlpwdmg.sql", new_path)
        if(os.path.exists(SQLNET_ORA)):
            self.col.printGreen(u"脚本已找到sqlnet.ora存在:   %s\n"%SQLNET_ORA)
            return [new_path, SQLNET_ORA]
        else:
            self.col.printGreen(u"脚本未找到sqlnet.ora不存在\n")
            return [new_path]

    def buding_echo(self):
        server_path = self.getpath()
        buding_path = server_path[0] + "//OPatch//opatch.bat lsinventory -all -detail"
        self.col.printGreen(u"已找到补丁脚本，正在启动！runing！\n")
        self.col.printGreen(u"补丁脚本路径： %s\n"%buding_path)
        os.system(buding_path)

    def check_file(self, filename, ser_path):
        filepath_name = "rdbms/admin/"+filename
        if os.path.exists(ser_path+filepath_name):
            self.col.printGreen(u"脚本已找到%s存在：    %s\n"%(filename, ser_path+filepath_name))
        else:
            self.col.printGreen(u"脚本未找到%s不存在\n"%filename)

    def run_sql(self, command):
        self.mysql = self.conn_oracle().cursor()
        if command == "":
            return ""
        try:
            self.mysql.execute(command)
            self.content = self.mysql.fetchall()
            self.mysql.close()
            return self.content
        except Exception as e:
            self.content = [e, ""]
            return self.content


    def create_excel_data(self):
        dict = self.create_dict()
        result = {}
        for d in tqdm(range(0, len(dict)), desc=u"正在执行sql!!!!!!!!"):
            time.sleep(1)
            if d == 0:
                result["D%s" % (d + 2)] = oracle_Level2.check_password_setting([self.run_sql(dict[d]), dict[d]])
            elif d == 1:
                result["D%s" % (d + 2)] = oracle_Level2.check_login_failed([self.run_sql(dict[d]), dict[d]])
            elif d == 2:
                result["D%s" % (d + 2)] = oracle_Level2.check_remote_login([self.run_sql(dict[d]), dict[d]])
            elif d == 3:
                result["D%s" % (d + 2)] = oracle_Level2.check_user_grantee(self.get_grantee())
            elif d == 4:
                result["D%s" % (d + 2)] = oracle_Level2.check_userpass([self.run_sql(dict[d]), dict[d]])
            elif d == 5:
                result["D%s" % (d + 2)] = oracle_Level2.check_user_open([self.run_sql(dict[d]), dict[d]])
            elif d == 6:
                result["D%s" % (d + 2)] = oracle_Level2.check_Label_Security([self.run_sql(dict[d]), dict[d]])
            elif d == 7:
                result["D%s" % (d + 2)] = oracle_Level2.check_audit_open([self.run_sql(dict[d]), dict[d]])
            elif d == 8:
                result["D%s" % (d + 2)] = oracle_Level2.check_value()
            elif d == 9:
                result["D%s" % (d + 2)] = oracle_Level2.check_value()
            elif d == 10:
                result["D%s" % (d + 2)] = oracle_Level2.check_audit_value([self.run_sql(dict[d]), dict[d]])
            elif d == 11:
                result["D%s" % (d + 2)] = oracle_Level2.check_version([self.run_sql(dict[d]), dict[d]])
        return result

    def check_statue(self):
        """
        ＠函数方法:检测错误
        :return: 
        """
        self.data = self.conlist
        try:
            tns_name = cx_Oracle.makedsn(self.conlist[2], self.conlist[3], "%s"%self.xe)
            cx_Oracle.connect(self.conlist[0], self.conlist[1], tns_name)
            return (10086, 'access')
        except Exception as e:
            return e



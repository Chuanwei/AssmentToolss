#encoding = utf-8

import hashlib
import color1
import colors
import platform
import Libs
from Libs import Database_mysql,Database_Oracle,Datebase_Sqlserver
from Libs.OS.Linux.Linux_readhat import *


class OS(object):


    def __init__(self):
        pass

    def os_info(self):
        os_str = platform.system()
        if(os_str == "Windows"):
            return platform.uname()
        elif(os_str == "Linux"):
            return platform.uname()
        else:
            return platform.uname()

    def get_col(self):
        if self.os_info()[0] == "Windows":
            return color1.colors()
        else:
            return colors.Color()

    def hash_tag(self, tag):
        m = hashlib.md5()
        m.update(tag)
        return m.hexdigest()

    def get_database_conn(self, chose_hash, conn):
        '''
        @typeid  int    1:mysql 2:sqlserver 3:oracle
        :cursor()
        '''
        if chose_hash == self.hash_tag("mysql"):
            return Database_mysql.Database(conn["username"], conn["password"], conn["host"], conn["port"])
        elif chose_hash == self.hash_tag("oracle"):
            return Database_Oracle.database_oracle(conn["username"], conn["password"], conn["host"], conn["port"], conn["xe"])
        elif chose_hash == self.hash_tag("redhat"):
            return ReadHat(conn["host"], conn["port"], conn["username"], conn["password"])

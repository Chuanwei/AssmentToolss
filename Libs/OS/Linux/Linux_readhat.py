#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import tqdm
from tqdm import tqdm,trange
import paramiko
import re

from function import RedHat_level2


class ReadHat(object):

    def __init__(self,host,port,username,password):
        self.config=[host,port,username,password]
        self.tag = "ReadHat"
        self.savename = self.config[0] + "-" + self.tag + "-" + time.strftime('%Y-%m-%d',
                                                                                 time.localtime(time.time()))

    def ReadHat(self):
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(self.config[0],22,self.config[2],self.config[3],timeout=5)
            return ssh
        except Exception as e :
            return {'statue':False,'msg':u'SSH连接错误!!!%s'%e}
    def cmd(self,command):
        if command == "":
            return ""
        ssh=self.ReadHat()
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            read =stdout.read()
            ssh.close()
            return read
        except:
            return ""

    def cmds(self,commands=[]):
        res =[]
        for i in commands:
            res.append(self.cmd(i))
        return res
    def create_dict(self):
        command_dict=["cat /etc/passwd && cat /etc/shadow",
                      "cat /etc/login.defs",
                      "cat /etc/pam.d/system-auth",
                      "service --status-all |grep running",
                      "awk -F: \'$3==0 {print $1}\' /etc/passwd",
                      "ls -l /etc/shadow&&ls -l /etc/passwd&&ls -l /etc/rc3.d&&ls -l /etc/profile",
                      "cat /etc/shadow",
                      "cat /etc/passwd",
                      "service --status-all | grep running",
                      "",
                      [ "tail -n 2 /var/log/messages",
                        "tail -n 2 /var/log/secure",
                        "tail -n 2 /var/log/maillog",
                        "tail -n 2 /var/log/cron"],
                      "ls -l /var/log/secure&&ls -l /var/log/maillog&&ls -l /var/log/cron&&ls -l /var/log/spooler&&ls -l /var/log/boot.log&&ls -l /var/log/messages",
                      [ "tail -n 2 /var/log/messages",
                        "tail -n 2 /var/log/secure",
                        "tail -n 2 /var/log/maillog",
                        "tail -n 2 /var/log/cron"],
                      "service --status-all | grep running,rpm -qa |grep patch",
                      ["cat /etc/hosts.deny","cat /etc/hosts.allow"],#这里使用的是cmds函数
                      "cat /etc/profile",
                      "cat /etc/security/limits.conf"]
        return command_dict

    def get_password_about(self):
        command = ["cat /etc/passwd","awk -F: '($2 = "") { print $1 }' /etc/shadow"]
        content = self.cmds(command)
        return [content, command]

    def get_buding(self):
        command = ['service --status-all | grep running','rpm -qa |grep patch']
        content = self.cmds(command)
        return [content, command]

    def get_audit_logfile(self):
        command = "cat /etc/audit/auditd.conf"
        try:
            result = self.cmd(command)
            log_file = re.findall(r'\nlog_file(.*?)\n', result)
            try:
                log_file = log_file[0].split("=")[1]
            except:
                log_file = log_file
            log_file = log_file.strip()
            log_result_command = "tail -n 3 " + log_file
            log_10lines = self.cmd(log_result_command)
            return [log_10lines, [command, log_result_command]]
        except:
            return ["", ["", ""]]


    def get_value(self, list):
        content = self.cmds(list)
        return [content, list]

    def create_excel_data(self):
        dict = self.create_dict()
        result = {}
        for d in tqdm(range(0, len(dict)), desc=u"正在执行命令!!!!!!!"):
            if d == 0:
                result["D%s" % (d + 2)] = RedHat_level2.check_pass_about(self.get_password_about())
            elif d == 1:
                result["D%s" % (d + 2)] = RedHat_level2.check_pass_set_about([dict[d], self.cmd(dict[d])])
            elif d == 2:
                result["D%s" % (d + 2)] = RedHat_level2.check_about_login([dict[d], self.cmd(dict[d])])
            elif d == 3:
                result["D%s" % (d + 2)] = RedHat_level2.check_hacking([dict[d], self.cmd(dict[d])])
            elif d == 4:
                result["D%s" % (d + 2)] = RedHat_level2.check_pass_empty([dict[d], self.cmd(dict[d])])
            elif d == 5:
                result["D%s" % (d + 2)] = RedHat_level2.check_permissions([dict[d], self.cmd(dict[d])])
            elif d == 6:
                result["D%s" % (d + 2)] = RedHat_level2.check_default_password([dict[d], self.cmd(dict[d])])
            elif d == 7:
                # print RedHat_level2.check_other_user([dict[d], self.cmd(dict[d])])["content"]
                result["D%s" % (d + 2)] = RedHat_level2.check_other_user([dict[d], self.cmd(dict[d])])
            elif d == 8:
                result["D%s" % (d + 2)] = RedHat_level2.check_log_user([dict[d], self.cmd(dict[d])])
            elif d == 9:
                result["D%s" % (d + 2)] = RedHat_level2.check_rizhiquanxian([dict[d], self.cmd(dict[d])])
            elif d== 10:
                result["D%s" % (d + 2)] = RedHat_level2.check_audit_log(self.get_audit_logfile())
            elif d== 11:
                result["D%s" % (d + 2)] = RedHat_level2.check_rizhiquanxian([dict[d], self.cmd(dict[d])])
            elif d == 12:
                result["D%s" % (d + 2)] = RedHat_level2.check_audit_date(self.get_value(dict[d]))
            elif d == 13:
                result["D%s" % (d + 2)] = RedHat_level2.check_buding(self.get_buding())
            elif d == 14:
                result["D%s" % (d + 2)] = RedHat_level2.check_ip(self.get_value(dict[d]))
            elif d == 15:
                result["D%s" % (d + 2)] = RedHat_level2.check_timout([dict[d], self.cmd(dict[d])])
            elif d== 16:
                result["D%s" % (d + 2)] = RedHat_level2.check_ziyuan([dict[d], self.cmd(dict[d])])
        return result

    def check_statue(self):
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(self.config[0],int(self.config[1]),self.config[2],self.config[3],timeout=5)
            return (10086, 'access')
        except Exception as e :
            return e




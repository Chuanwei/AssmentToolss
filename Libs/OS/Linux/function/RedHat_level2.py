#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
def check_pass_about(command=[]):
        """应对登录操作系统和数据库系统的用户进行身份标识和鉴别
        cat /etc/passwd && cat /etc/shadow"""
        content = ""
        commanda = ""
        try:
            a = re.findall(r'.*?[5,9]\d{2}.*/.*',command[0][0])
            for i in a:
                content += "%s\n"%i
            b =u"匹配大于500的账号:\n%s\n"%content
            if len(command[0][1]) ==0:
                b+=u"没有空密码的用户"
            else:
                b+=u"存在空密码的用户:%s"%command[0][1]
            for i in command[1]:
                commanda += i + "\n"
            return {"command":commanda,"content":b}
        except AttributeError :
            return {"command": commanda, "content": u"此条命令执行失败"}
def check_pass_set_about(command = []):
        """
        操作系统和数据库系统管理用户身份标识应具有不易被冒用的特点，口令应有复杂度要求并定期更换；
        cat /etc/login.defs
        """
        try:
            a =re.findall(r'PASS_MAX_DAYS.*?(\d{1,7})',command[1])
            b=re.findall(r'PASS_MIN_DAYS.*?(\d{1,7})',command[1])
            c = re.findall(r'PASS_MIN_LEN.*?(\d{1,7})', command[1])
            d = re.findall(r'PASS_WARN_AGE.*?(\d{1,7})', command[1])
            content="PASS_MAX_DAYS:%s\n"%a
            content+="PASS_MIN_DAYS:%s\n"%b
            content+="PASS_MIN_LEN:%s\n"%c
            content+="PASS_WARN_AGE:%s\n"%d
            return {"command":command[0],"content":content}
        except AttributeError:
            return {"command": "", "content": u"此条命令执行失败"}

def check_about_login(command=[]):
    """应启用登录失败处理功能，可采取结束会话、限制非法登录次数和自动退出等措施；
    cat /etc/pam.d/system-auth
    """
    try:
        content = "登录多少次以后拒绝登录，并锁定账号:\n"
        a =re.findall(r'auth.*required+.*\n',command[1])
        b = re.findall(r'account.*required.*\n', command[1])
        for i in a:
            content = i+"\n"
        for t in b:
            content+=u'登录多少次次失败以后，则拒绝访问:\n%s'%t + "\n"
        return {"command":command[0],"content":content}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}
def check_hacking(command=[]):
    """
    当对服务器进行远程管理时，应采取必要措施，防止鉴别信息在网络传输过程中被窃听；
    """
    try:
        result = u"开启了telnet服务" if "telnet" in command[1] else u"未开启telnet服务"
        return {"command":command[0], "content":result}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}


def check_pass_empty(command=[]):
    """应为操作系统和数据库系统的不同用户分配不同的用户名，确保用户名具有唯一性；
    awk -F: \'$3==0 {print $1}\' /etc/passwd"""
    try:
        s ="UID为0的用户为:%s"%command[1]
        return {"command": command[0], "content": s}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}
def check_permissions(command=[]):
    """
    ls -l /etc/shadow&&ls -l /etc/passwd&&ls -l /etc/rc3.d&&ls -l /etc/profile
    应启用访问控制功能，依据安全策略控制用户对资源的访问；
    """
    try:
        return {"command":command[0],"content":command[1]}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}
def check_default_password(command=[]):
    """
    应严格限制默认账户的访问权限，重命名系统默认账户，修改这些账户的默认口令；
    cat /etc/shadow
    """
    try:
        password =re.findall(r'(.*\$.*)',command[1])
        content = ""
        for i in password:
            content += i
        request ="限制了默认账号的访问权限:\n%s"%content
        return {"command":command[0],"content":request}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}

def check_other_user(command=[]):
    """
    应及时删除多余的、过期的账户，避免共享账户的存在
    cat /etc/passwd
    """
    try:
        request=command[1]
        content = ""
        # for i in request:
        #     content += i
        return {"command":command[0],"content":request}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}

def check_log_user(command=[]):
    """
    service --status-all | grep running
    审计范围应覆盖到服务器和重要客户端上的每个操作系统用户和数据库用户:
    """
    try:
        res = re.findall(r'auditd.*|.*sys.*',command[1])
        content = ""
        for i in res:
            content += i + "\n"
        return {"command":command[0],"content":content}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}

def check_rizhiquanxian(command=[]):
    """
    审计记录应受到保护避免受到未预期的删除、修改或覆盖等。
    ls -l /var/log/secure&&ls -l /var/log/maillog&&ls -l /var/log/cron&&ls -l /var/log/spooler&&ls -l /var/log/boot.log&&ls -l /var/log/messages
    """
    try:
        return {"command":command[0],"content":command[1]}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}
def check_buding(command=[]):
    """
    操作系统应遵循最小安装的原则，仅安装需要的组件和应用程序，并通过设置升级服务器等方式保持系统补丁及时得到更新。
    service --status-all | grep running,rpm -qa |grep patch
    """
    try:
        res = u'正在运行的服务为:\n%s'%command[0][0]
        res+=u'系统补丁为:\n%s'%command[0][1]
        commands = ""
        for i in command[1]:
            commands += i + "\n"
        return {"command":commands,"content":res}
    except:
        return {"command": "", "content": u"此条命令执行失败"}
def check_ip(command=[]):
    """
    应通过设定终端接入方式、网络地址范围等条件限制终端登录；
    cat /etc/hosts.deny,cat /etc/hosts.allow
    """
    try:
        res=u'接入方式为：\n%s'%command[0][0]
        res+=u'服务器登录范围：\n%s'%command[0][1]
        return {"command":command[1][0],"content":res}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}

def check_timout(command=[]):
    """
    应根据安全策略设置登录终端的操作超时锁定；
    cat /etc/profile
    """
    try:
        result = ""
        res =re.findall(r'.*TMOUT.*',command[1])
        if len(res)==0:
            result = u'未发现TMOUT'
            return {"command":command[0], "content":result}
        else:
            return {"command":command[0],"content":res}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}

def check_ziyuan(command=[]):
    """
    应限制单个用户对系统资源的最大或最小使用限度；
    cat /etc/security/limits.conf
    """
    try:
        content = ""
        res =re.findall(r'.*soft.*|.*hard.*|.*student.*',command[1])
        for i in res:
            content += i + "\n"
        return {"command":command[0],"content":content}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}


def check_audit_log(command_result = []):
    """
    @函数方法:查找审计配置文件，并且查看相关日志记录
    :param command_result: 
    :return: 
    """
    try:
        audit_type = re.findall(r'type=(.*?) ', command_result[0])
        command = ""
        for i in command_result[1]:
            command += i + "\n"
        return {"command":command, "content":command_result[0]}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}


def check_audit_date(command_result):
    """
    @函数方法:查看具体审计记录，查看是否具体到时间日期
    :param command_result: 
    :return: 
    """
    try:
        sql = ""
        content = ""
        for i in command_result[1]:
            sql += i + "\n"
        for n in range(0, len(command_result[0])):
            content += command_result[0][n]
        # for n in command_result[0]:
        return {"command":sql, "content":content}
    except AttributeError:
        return {"command": "", "content": u"此条命令执行失败"}

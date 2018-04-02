#encoding:utf-8
"""
@author:Liod
@file:oracle_Level2.py
@time:17-12-25下午3:10
"""

def check_login_failed(sql_result=[]):
    """
    @函数功能:检测数据库登录失败处理情况
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    login_lock_num = sql_result[0][0][1]
    lock_day = sql_result[0][1][1]
    result = u"经过检查数据库设置登录失败次数:{0}次, 口令锁定时间为:{1}天".format(login_lock_num, lock_day)
    return {"command":sql_result[1], "content":result}

def check_user_open(sql_result=[]):
    """
    @函数功能:检查数据库开启的用户信息情况
    :param sql_result: 
    :return: 
    """
    result = ""
    for ms in sql_result[0]:
        result += "%-20s:   open \n"%ms[0]
    return {"command":sql_result[1], "content":result}

def check_password_setting(sql_result=[]):
    """
    @函数功能:检测数据库密码设置策略
    传入　[[(), ()], ["", ""]]
    检查口令
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    result = "%-30s%-15s   %-15s \n"%("PASSWORD_VERIFY_FUNCTION", sql_result[0][0][0], u"启用了口令复杂函数" if sql_result[0][0][0] != "NULL" else u"未启用口令复杂函数")
    result += "%-30s%-15s   %-15s \n"%("PASSWORD_LIFE_TIME", sql_result[0][1][0], u"启用了口令过期时限" if sql_result[0][1][0] != "UNLIMITED" else u"未启用口令过期时限")
    return {"command":sql_result[1], "content":result}

def check_remote_login(sql_result=[]):
    """
    @函数功能:查看数据库是否允许连接的情况
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    :param sql_result: 
    :return: 
    """
    result = "%-18s：     %-10s      %s"%(sql_result[0][0][0], sql_result[0][0][1], u"允许远程登录" if sql_result[0][0][1] == "TRUE" else u"不允许远程登录")
    return {"command":sql_result[1], "content":result}


def check_userpass(sql_result=[]):
    """
    @函数功能:检测用户名账号密码情况 
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    :param sql_result: 
    :return: 
    """
    result = ""
    if len(sql_result[0]) == 0:
        result += "未存在默认账号的情况"
    else:
        for i in sql_result[0]:
            result += "存在默认账号:  %s \n"%i[0]
    return {"command":sql_result[1], "content":result}


def check_user_priv(sql_result=[]):

    """
    @函数功能:检测用户身份开启情况
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    :param sql_result: 
    :return: 
    """
    result = ""
    for o in sql_result[0]:
        result += "账号:%-10s         状态:%s \n"%(o[0], o[1])
    return {"command":sql_result[1], "content":result}

def check_audit_open(sql_result=[]):
    """
    @函数功能:检测用户审计开启情况
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    :param sql_result: 
    :return: 
    """

    result = ""
    if sql_result[0][0][0] in ["DB", 'DB,Extended', "OS"]:
        result += "%s   %-15s    %s"%(u"数据库已开启审计", "audit_trail", sql_result[0][0][0])
    elif sql_result[0][0][0] in ["None"]:
        result += "%s   %-15s    %s"%(u"数据库未开启审计", "audit_trail", sql_result[0][0][0])
    else:
        result += "%s   %-15s    %s" % (u"数据库未开启审计", "audit_trail", sql_result[0][0][0])
    return {"command":sql_result[1], "content":result}


def check_user_grantee(sql_result = []):
    """
    @函数功能:检测数据库用户在系统上，表权限，和用户自身具有的权限
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    :param sql_result: 
    """
    result = ""
    command = ""
    content = sql_result[0]
    for i in content:
        for p in i:
            result += "用户名:%-15s    权限:%s\n"%(p[0], p[1])
    for sql in sql_result[1]:
        command += sql + "\n"
    # print result
    return {"command":command, "content":result}

def check_Label_Security(sql_result=[]):
    """
    @函数功能:检测是否安装敏感标记模块
    :param sql_result: 
    :return: 
    """
    result = ""
    if sql_result[0][0][0] == "FALSE":
        result = "Oracle Label Security模块未安装"
    else:
        result = "Oracle Label Security模块安装，数据库自身保护了审计进程"
    return {"command":sql_result[1], "content":result}




def check_audit_value(sql_result = []):
    """
    @函数功能，检测审计保护进程audit value是否安装
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    :param sql_result: 
    """

    a = sql_result[0][0][0]
    if a in ('NONE', 'FALSE'):
        result = "Oracle Database Vault模块未安装"
    else:
        result = "Oracle Database Vault模块安装，数据库自身保护了审计进程"
    return {"command":sql_result[1], "content":result}

def check_audit_descdate():
    """
    @函数功能:检测审计记录是否具体到具体的ip,时间
    :return: 
    """
    pass

def check_version(sql_result=[]):
    """
    @函数功能:查看数据库版本信息
    :param sql_result: 
    :return: 
    """
    result = ""
    for res in sql_result[0]:
        result += "%s \n"%res[0]
    return {"command":sql_result[1], "content":result}

def check_value():
    """
    @暂时返回空
    :return: 
    """
    return {"command":"world", "content":u"暂未开发"}
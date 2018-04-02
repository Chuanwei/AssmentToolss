#encoding:utf-8
"""
@author:Liod
@file:mysql_Level2.py
@time:17-12-22下午1:52
"""


def check_audit(sql_result=[]):
    """
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    if sql_result[0] == "":
        return {"command":sql_result[1], "content":u"命令执行失败"}
    result = ""
    result += "%-20s      %-15s \n"%(sql_result[0][32][0], u"未开启" if sql_result[0][32][1] == "OFF" else u"开启")
    result += "%-20s      %-15s \n"%(sql_result[0][15][0], u"未开启" if sql_result[0][15][1] == "OFF" else u"开启")
    result += "%-20s      %-15s \n"%(sql_result[0][38][0], sql_result[0][38][1])
    # print result
    return {"command":sql_result[1], "content":result}

def check_ssl(sql_result=[]):
    """

    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    if sql_result[0] == "":
        return {"command":sql_result[1], "content":u"命令执行失败"}
    if sql_result[0][0][1] == "DISABLED":
        return {"command":sql_result[1], "content":"%s    DISABLED"%sql_result[0][0][0]}
    else:
        return {"command": sql_result[1], "content":"%s   %10s"%(sql_result[0][0][0], sql_result[0][0][1])}

def check_uservoid(sql_result=[]):
    """
    
    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    if sql_result[0] == "":
        return {"command":sql_result[1], "content":u"命令执行失败"}
    result = ""
    root = "*81F5E21E35407D884A6CD4A731AEBFB6AF209E1B"
    for res in sql_result[0]:
        res = list(res)
        if res[2]== '':
            res[2] = u"空口令"
        elif res[2] == root:
            res[2] = u"弱口令"
        else:
            res[2] = u"密码符合"
        result +="%-10s    %-20s         %s"%(res[0], res[1], res[2])+" \n"
        result.replace("", ".")
    return {"command":sql_result[1], "content":result}

def check_skip(sql_result = []):
    """

    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    if sql_result[0] == "":
        return {"command":sql_result[1], "content":u"命令执行失败"}
    result = "%s    %10s"%(sql_result[0][0][0], u"未开启" if sql_result[0][0][1] == "OFF" else u"开启")
    return {"command":sql_result[1], "content":result}

def check_userRights(sql_result):
    """
    :sqllist = [[], []]: 
    :return {"content":"" "command":""}: 
    """
    if sql_result[0] == "":
        return {"command":sql_result[1], "content":u"命令执行失败"}
    result = ""
    sql = ""
    for i in sql_result[0][0]:
        result += i[0] + "\n"
    for s in sql_result[1]:
        sql += s + "\n"
    return {"command":sql, "content":result}

def check_terminal_ReadHat(sql_result = []):
    """

    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    if sql_result[0] == "":
        return {"command":sql_result[1], "content":u"命令执行失败"}
    result = "%s     %10s"%(sql_result[0][0][0], sql_result[0][0][1])
    return {"command":sql_result[1], "content":result}

def check_terminal_setting(sql_result=[]):
    """

    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    if sql_result[0] == "":
        return {"command":sql_result[1], "content":u"命令执行失败"}
    result = ""
    root = "*81F5E21E35407D884A6CD4A731AEBFB6AF209E1B"
    for res in sql_result[0]:
        res = list(res)
        if res[0]== '%':
            res[2] = u"允许任意方式"
        result +="%s     %20s        %16s"%(res[0], res[1], res[2])+" \n"
    return {"command": sql_result[1], "content": result}


def check_version(sql_result=[]):
    """

    :sql_result= [(())sql命令执行产生的二维元组, "sql命令"]: 
    :return {"content":"" "command":""}: 
    """
    if sql_result[0] == "":
        return {"command":sql_result[1], "content":u"命令执行失败"}
    result = "%s"%(sql_result[0][0][0])
    return {"command":sql_result[1], "content":result}

def hello():
    print "hello"


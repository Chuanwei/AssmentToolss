# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Color(object):
    '''
        说明：
        前景色            背景色           颜色
        ---------------------------------------
        30                40              黑色
        31                41              红色
        32                42              绿色
        33                43              黃色
        34                44              蓝色
        35                45              紫红色
        36                46              青蓝色
        37                47              白色
        显示方式           意义
        -------------------------
        0                终端默认设置
        1                高亮显示
        4                使用下划线
        5                闪烁
        7                反白显示
        8                不可见

    '''

    def __init__(self):
        pass

    def printRed(self, formatString):
        sys.stdout.write("\033[31;1m{}\033[0m".format(formatString))

    def printGreen(self, formatString):
        sys.stdout.write("\033[32;1m{}\033[0m".format(formatString))

    def printBlue(self, formatString):
        sys.stdout.write("\033[34;1m{}\033[0m".format(formatString))

    def inputRed(self, formatString):
        return raw_input("\033[31;1m{}\033[0m".format(formatString))

    def inputGreen(self, formatString):
        return raw_input("\033[32;1m{}\033[0m".format(formatString))




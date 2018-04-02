# coding=utf-8

import ctypes, sys
class colors(object):


    def __init__(self):

        self.STD_INPUT_HANDLE = -10
        self.STD_OUTPUT_HANDLE = -11
        self.STD_ERROR_HANDLE = -12

# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
# 由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

# Windows CMD命令行 字体颜色定义 text colors
        self.FOREGROUND_BLACK = 0x00  # black.
        self.FOREGROUND_DARKBLUE = 0x01  # dark blue.
        self.FOREGROUND_DARKGREEN = 0x02  # dark green.
        self.FOREGROUND_DARKSKYBLUE = 0x03  # dark skyblue.
        self.FOREGROUND_DARKRED = 0x04  # dark red.
        self.FOREGROUND_DARKPINK = 0x05  # dark pink.
        self.FOREGROUND_DARKYELLOW = 0x06  # dark yellow.
        self.FOREGROUND_DARKWHITE = 0x07  # dark white.
        self.FOREGROUND_DARKGRAY = 0x08  # dark gray.
        self.FOREGROUND_BLUE = 0x09  # blue.
        self.FOREGROUND_GREEN = 0x0a  # green.
        self.FOREGROUND_SKYBLUE = 0x0b  # skyblue.
        self.FOREGROUND_RED = 0x0c  # red.
        self.FOREGROUND_PINK = 0x0d  # pink.
        self.FOREGROUND_YELLOW = 0x0e  # yellow.
        self.FOREGROUND_WHITE = 0x0f  # white.

# Windows CMD命令行 背景颜色定义 background colors
        self.BACKGROUND_BLUE = 0x10  # dark blue.
        self.BACKGROUND_GREEN = 0x20  # dark green.
        self.BACKGROUND_DARKSKYBLUE = 0x30  # dark skyblue.
        self.BACKGROUND_DARKRED = 0x40  # dark red.
        self.BACKGROUND_DARKPINK = 0x50  # dark pink.
        self.BACKGROUND_DARKYELLOW = 0x60  # dark yellow.
        self.BACKGROUND_DARKWHITE = 0x70  # dark white.
        self.BACKGROUND_DARKGRAY = 0x80  # dark gray.
        self.BACKGROUND_BLUE = 0x90  # blue.
        self.BACKGROUND_GREEN = 0xa0  # green.
        self.BACKGROUND_SKYBLUE = 0xb0  # skyblue.
        self.BACKGROUND_RED = 0xc0  # red.
        self.BACKGROUND_PINK = 0xd0  # pink.
        self.BACKGROUND_YELLOW = 0xe0  # yellow.
        self.BACKGROUND_WHITE = 0xf0  # white.
        self.std_out_handle = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)


    def set_cmd_text_color(self, color):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(self.std_out_handle, color)
        return Bool


    # reset white
    def resetColor(self):
        self.set_cmd_text_color(self.FOREGROUND_RED | self.FOREGROUND_GREEN | self.FOREGROUND_BLUE)


###############################################################

# 蓝色
# blue
    def printBlue(self, mess=""):
        self.set_cmd_text_color(self.FOREGROUND_BLUE)
        sys.stdout.write(mess)
        self.resetColor()
    def inputBlue(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_BLUE)
        sys.stdout.write(mess)
        self.resetColor()
        return sys.stdin.readline().strip()


# 绿色
# green
    def printGreen(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_GREEN)
        sys.stdout.write(mess)
        self.resetColor()



    def inputGreen(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_GREEN)
        sys.stdout.write(mess)
        self.resetColor()
        return sys.stdin.readline().strip()
# 天蓝色
# sky blue
    def printSkyBlue(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_SKYBLUE)
        sys.stdout.write(mess)

        self.resetColor()


# 红色
# red
    def printRed(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_RED)
        sys.stdout.write(mess)
        self.resetColor()

    def inputRed(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_RED)
        sys.stdout.write(mess)
        self.resetColor()
        return sys.stdin.readline().strip()


# 粉红色
# pink
    def printPink(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_PINK)
        sys.stdout.write(mess)
        return self.resetColor()



# 黄色
# yellow
    def printYellow(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_YELLOW)
        sys.stdout.write(mess)
        self.resetColor()


# 白色
# white
    def printWhite(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_WHITE)
        sys.stdout.write(mess)
        self.resetColor()


##################################################

# 白底黑字
# white bkground and black text
    def printWhiteBlack(self, mess):
        self.set_cmd_text_color(self.FOREGROUND_BLACK | self.BACKGROUND_WHITE)
        sys.stdout.write(mess)
        self.resetColor()


# 白底黑字
# white bkground and black text
    def printWhiteBlack_2(self, mess):
        self.set_cmd_text_color(0xf0)
        sys.stdout.write(mess)
        self.resetColor()


# 黄底蓝字
# white bkground and black text
    def printYellowRed(self, mess):
        self.set_cmd_text_color(self.BACKGROUND_YELLOW | self.FOREGROUND_RED)
        sys.stdout.write(mess)
        self.resetColor()


##############################################################
#
# test = colors()
# if test.printPink(u'printDarkBlue:暗蓝色文字'.encode('gb2312')) is None:
#      print "ok"
#    # printDarkGreen(u'printDarkGreen:暗绿色文字\n'.encode('gb2312'))
#    # printDarkSkyBlue(u'printDarkSkyBlue:暗天蓝色文字\n'.encode('gb2312'))
#    # printDarkRed(u'printDarkRed:暗红色文字\n'.encode('gb2312'))
#    # printDarkPink(u'printDarkPink:暗粉红色文字\n'.encode('gb2312'))
#    # printDarkYellow(u'printDarkYellow:暗黄色文字\n'.encode('gb2312'))
#    # printDarkWhite(u'printDarkWhite:暗白色文字\n'.encode('gb2312'))
#    # printDarkGray(u'printDarkGray:暗灰色文字\n'.encode('gb2312'))
#    # printBlue(u'printBlue:蓝色文字\n'.encode('gb2312'))
#    # printGreen(u'printGreen:绿色文字\n'.encode('gb2312'))
#    # printSkyBlue(u'printSkyBlue:天蓝色文字\n'.encode('gb2312'))
#    # printRed(u'printRed:红色文字\n'.encode('gb2312'))
#    # printPink(u'printPink:粉红色文字\n'.encode('gb2312'))
#    # printYellow(u'printYellow:黄色文字\n'.encode('gb2312'))
#    # printWhite(u'printWhite:白色文字\n'.encode('gb2312'))
#    #
#    # printWhiteBlack(u'printWhiteBlack:白底黑字输出\n'.encode('gb2312'))
#    # printWhiteBlack_2(u'printWhiteBlack_2:白底黑字输出（直接传入16进制参数）\n'.encode('gb2312'))
#    # printYellowRed(u'printYellowRed:黄底红字输出\n'.encode('gb2312'))
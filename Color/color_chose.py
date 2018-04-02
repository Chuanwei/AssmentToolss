import platform
import colors
import color1

class chose_color(object):
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

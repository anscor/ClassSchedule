#!python3
# -*- coding: utf-8 -*-
'''
@Author: Anscor
@LastEditors: Anscor
@Description: 配置文件
@Date: 2019-03-13
@LastEditTime: 2019-03-22
'''

# ----------CONFIG----------

# 是否处于调试状态，正常使用时请置为False
DEBUG = False

# 账号、密码
USER = ""
PASSWORD = ""

# 课程开始时间（第一周周一）
SYEAR = 2019
SMONTH = 2
SDAY = 18

# 浏览器路径
EXEC_PATH = "D:/Anscor/Google/chromedriver.exe"

# JWC网址
JWC_URL = "http://202.202.1.41"

# 实验课程syjx网址
SYJX_URL = "http://syjx.cqu.edu.cn"

# ----------END CONFIG----------


# 一周7天对应
WEEKDAYS = ["", u"一", u"二", u"三", u"四", u"五", u"六", u"日"]

# 上课时间
S_TIMES = {
    1: "080000",
    2: "085500",
    3: "101000",
    4: "110500",
    5: "143000",
    6: "152500",
    7: "164000",
    8: "173500",
    9: "193000",
    10: "202500",
    11: "212000"
}

# 下课时间
E_TIMES = {
    1: "084500",
    2: "094000",
    3: "105500",
    4: "115000",
    5: "151500",
    6: "161000",
    7: "172500",
    8: "182000",
    9: "201500",
    10: "211000",
    11: "220500"
}

# 实验课上课时间
ES_TIMES = {
    1: "083000",
    2: "091500",
    3: "100000",
    4: "104500",
    5: "143000",
    6: "151500",
    7: "160000",
    8: "164500",
    9: "190000",
    10: "194500",
    11: "203000",
    12: "211500"
}

# 实验课下课时间
EE_TIMES = {
    1: "091500",
    2: "100000",
    3: "104500",
    4: "113000",
    5: "151500",
    6: "160000",
    7: "164500",
    8: "173000",
    9: "194500",
    10: "203000",
    11: "211500",
    12: "220000"
}

# 如果处于调试时，从配置文件中读入账号、密码


def init():
    if DEBUG:
        import json
        import codecs
        f = codecs.open("./config.json")
        info = json.load(f)
        global USER, PASSWORD
        USER = info["USER"]
        PASSWORD = info["PASSWORD"]

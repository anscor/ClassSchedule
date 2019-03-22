#!python3
# -*- coding: utf-8 -*-
'''
@Author: Anscor
@LastEditors: Anscor
@Description: 主函数
@Date: 2019-03-13
@LastEditTime: 2019-03-22
'''

import Config
from CourseControler import CourseControler
from CalendarMaker import CadenlarMaker
import codecs

if __name__ == "__main__":
    Config.init()
    cctl = CourseControler()
    courses = cctl.GetCourse()
    cm = CadenlarMaker(courses=courses)
    f = codecs.open("./ClassSchedule.ics", "w", "utf-8")
    f.write(cm.Make())
    f.close()
        

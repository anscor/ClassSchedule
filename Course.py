#!python3
# -*- coding: utf-8 -*-
'''
@Author: Anscor
@LastEditors: Anscor
@Description: 课程类
@Date: 2019-03-13
@LastEditTime: 2019-03-13
'''

class Course:
    
    def __init__(self, course=None, start_time="", end_time="", location="", teacher="", name="", detail="", weeks="", day=""):
        if course != None:
            self.__initByCourse__(course)
        else:
            self.start_time = start_time
            self.end_time = end_time
            self.location = location
            self.teacher = teacher
            self.name = name
            self.detail = detail
            self.weeks = weeks
            self.day = day
    
    def __initByCourse__(self, course):
        self.start_time = course.start_time
        self.end_time = course.end_time
        self.location = course.location
        self.teacher = course.teacher
        self.name = course.name
        self.detail = course.detail
        self.weeks = course.weeks
        self.day = course.day

#!python3
# -*- coding: utf-8 -*-
'''
@Author: Anscor
@LastEditors: Anscor
@Description: 创建日历文件
@Date: 2019-03-22
@LastEditTime: 2019-03-22
'''

import Config
import datetime
from CalendarEvent import CalendarEvent
from Calendar import Calendar

class CadenlarMaker:
    def __init__(self, courses=None):
        self.courses = courses
        self.events = []
        self.calendar = None
        self.startDate = datetime.datetime(Config.SYEAR, Config.SMONTH, Config.SDAY)
    
    # 处理每个课程，返回日历事件列表
    def __CreateCourseEvents(self, course):
        events = []
        for w in course.weeks:
            # 计算日期
            days = (w - 1) * 7 + course.day - 1
            today = self.startDate + datetime.timedelta(days=days)
            # 创建事件
            event = CalendarEvent(
                dtstart=today.strftime("%Y%m%d") + "T" + course.start_time,
                dtend=today.strftime("%Y%m%d") + "T" + course.end_time,
                summary=course.name,
                location = course.location,
                desc=course.teacher + " " + course.detail
            )
            events.append(event)
        
        return events

    
    def Make(self):
        events = []
        for course in self.courses:
            events = events + self.__CreateCourseEvents(course=course)
        calendar = Calendar(events=events)
        return calendar.GetCalendar()

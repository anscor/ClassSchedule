#!python3
# -*- coding: utf-8 -*-
'''
@Author: Anscor
@LastEditors: Anscor
@Description: 日历文件
@Date: 2019-03-22
@LastEditTime: 2019-03-22
'''

class Calendar:
    def __init__(self, events=None):
        # 日历事件集合
        self.events = events
        # 日历头部信息说明
        self.header = [
            "BEGIN:VCALENDAR",
            "PRODID:-//Google Inc//Google Calendar 70.9054//EN",
            "VERSION:2.0",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:classSchedule",
            "X-WR-TIMEZONE:Asia/Shanghai",
            "BEGIN:VTIMEZONE",
            "TZID:Asia/Shanghai",
            "BEGIN:STANDARD",
            "TZOFFSETFROM:+0800",
            "TZOFFSETTO:+0800",
            "TZNAME:CST",
            "DTSTART:19700101T000000",
            "END:STANDARD",
            "END:VTIMEZONE"
        ]
        # 日历尾部结尾
        self.tail = "END:VCALENDAR"
    
    def GetCalendar(self):
        # 将日历事件转换为相应的字符串
        es = "".join([e.Event() for e in self.events])
        # 返回日历（字符串）
        return "\r\n".join(self.header) + "\r\n" + es + self.tail

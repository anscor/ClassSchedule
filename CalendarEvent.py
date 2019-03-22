#!python3
# -*- coding: utf-8 -*-
'''
@Author: Anscor
@LastEditors: Anscor
@Description: 日历事件
@Date: 2019-03-22
@LastEditTime: 2019-03-22
'''

class CalendarEvent:
    def __init__(self, dtstart, dtend, summary, location, desc):
        self.begin = "VEVENT"
        self.end = "VEVENT"
        self.event = {
            "BEGIN": "VEVENT",
            "DTSTART;TZID=Asia/Shanghai": dtstart,
            "DTEND;TZID=Asia/Shanghai": dtend,
            "SUMMARY": summary,
            "LOCATION": location,
            "DESCRIPTION": desc,
            "END": "VEVENT"
        }

    def Event(self):
        l = [":".join((key, value)) for key, value in self.event.items()]
        event = "\r\n".join(l) + "\r\n"
        return event

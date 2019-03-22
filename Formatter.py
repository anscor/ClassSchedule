#!python3
# -*- coding: utf-8 -*-
'''
@Author: Anscor
@LastEditors: Anscor
@Description: 格式化类，用于格式化时间、周次等
@Date: 2019-03-13
@LastEditTime: 2019-03-22
'''

import Config

class Formatter:
    def __init__(self):
        self.weekdays = Config.WEEKDAYS
        self.startTimes = Config.S_TIMES
        self.endTimes = Config.E_TIMES
        self.exp_startTimes = Config.ES_TIMES
        self.exp_endTimes = Config.EE_TIMES
    
    def FormatDay(self, time):
        # 获取周几
        # 将如 四[1-2节] 数据转换为数字 4 返回
        for i in range(0, len(self.weekdays)):
            if time[0] == self.weekdays[i]:
                return i
    
    # 获取每节课周次
    # 使用list存储所有周次
    def FormatWeek(self, week):
        # 处理形如 1,2,3 之类的数据
        week = week.split(',')

        weeks = []

        for w in week:
            # 处理形如 1-2 之类的数据
            w = w.split('-')
            # 开始周次
            startWeek = int(w[0])
            # 结束周次，初始值的开始周次相等，处理可能出现的单周次（课程只有一周有）
            endWeek = startWeek

            # 多周有课，设置结束周次
            if len(w) == 2:
                endWeek = int(w[1])

            # 依次将周次添加到list中
            for i in range(startWeek, endWeek + 1):
                weeks.append(i)

        return weeks
    
    # 格式化时间，将形如 周一[1-4节] 或 周一[1-4] 格式的上课节次转化为具体时间
    # kind 表示处理的数据类型，为0时表示处理的数据为正常理论课程，1表示为实验课程
    def FormatTime(self, time, kind=0):
        if kind == 1:
            time = time[time.find('[') + 1 : time.find(']')].split('-')
        else:
            time = time[time.find('[') + 1 : time.find(u'节')].split('-')

        # 处理结果代码，0表示成功，-1表示失败（不处理）
        code = 0
        
        # 只有一节，不存在，跳过
        if len(time) <= 1:
            code = -1
            return code, 0, 0
        
        # 超出范围的课，某些特殊课程会出现为13节
        if int(time[0]) < 1 or int(time[1]) > 12:
            code = -1
            return code, 0, 0

        sTime = 0
        eTime = 0
        # 特殊课程处理，为从开放实验课导入教务网的课程
        if kind == 1:
            code = 1
            sTime = self.exp_startTimes[int(time[0])]
            eTime = self.exp_endTimes[int(time[1])]
        # 正常课程转换为上、下课时间
        else:
            code = 0
            sTime = self.startTimes[int(time[0])]
            eTime = self.endTimes[int(time[1])]

        return code, sTime, eTime
        

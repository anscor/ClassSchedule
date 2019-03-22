#!python3
# -*- coding: utf-8 -*-

import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import lxml
import re
import json
import codecs
import datetime

# -----------CONFIG-----------

# 账号、密码
username = ""
password = ""
# 第一周周一时间（年，月，日）
startYear = 2019
startMonth = 2
startDay = 18
# 浏览器路径
executable_path = "D:/Anscor/Google/chromedriver.exe"
# 网站url
url = "http://202.202.1.41"

# -----------CONFIG-----------

# 一周7天对应
weekdays = ["", u"一", u"二", u"三", u"四", u"五", u"六", u"日"]

# 上课时间
sTimes = {1 : "080000", 
        3 : "101000", 
        5 : "143000", 
        7 : "164000", 
        9 : "193000"}

# 下课时间
eTimes = {2 : "094000", 
        4 : "115000", 
        6 : "161000", 
        8 : "182000", 
        10 : "211000", 
        12 : "220500"}

# 通过webdriver进行模拟点击，进行登录、选择课表等操作，获取课表界面网页内容
def GetOriginalCourse(username, password, executable_path, url):

    option = Options()
    option.add_argument("--headless")
    option.add_argument("--disable-gpu")

    # 使用Chrome进行模拟点击
    driver = webdriver.Chrome(
        executable_path=executable_path,
        chrome_options=option)
    driver.get(url)

    # 登录
    driver.switch_to_frame("frmLogin")

    # 用户名和密码，即学号与密码
    usr = driver.find_element_by_id("txt_dsdsdsdjkjkjc")
    pwd = driver.find_element_by_id("txt_dsdfdfgfouyy")

    # 填入数据
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element(usr)
    action.send_keys(username)
    action.move_to_element(pwd)
    action.send_keys(password)
    action.move_to_element(usr)
    # 执行
    action.perform()

    # 登录按钮点击
    driver.find_element_by_class_name("but20").submit()

    # 课表界面，选择课程安排
    driver.get("http://202.202.1.41/znpk/Pri_StuSel.aspx")
    btn = driver.find_elements_by_class_name("button")
    btn[1].click()

    driver.switch_to_frame("frmRpt")

    # 取得课表页面网页内容
    originalCourse = driver.page_source

    driver.close()

    return originalCourse

# 使用BeautifulSoup对网页内容进行处理，从中提取出课程信息（课程名称、老师、地点、时间等）
def ChangeCourse(originalCourse):
    bs = BeautifulSoup(originalCourse, "lxml")
    # 多页
    pages = bs.select(".content")

    coursesInfo = []

    for page in pages:
        # 课程信息表格
        page_tables = page.select(".page_table")

        for page_table in page_tables:
            # 过滤表头
            thead = page_table.select("thead")
            if len(thead) == 0:
                continue

            # 课程表格主体
            tbody = page_table.select("tbody")

            courses = tbody[0].select("tr")

            for course in courses:
                infos = course.select("td")
                # 正常课程（理论课）
                if len(infos) == 13:
                    courseName = str(infos[1].get_text())
                    teacherName = str(infos[9].get_text())
                    courseWeek = str(infos[10].get_text())
                    courseTime = str(infos[11].get_text())
                    courseLocation = str(infos[12].get_text())

                    # 同一课程，不同老师或不同时间教室不同等情况
                    if courseName == "":
                        courseName = str(infos[1]["hidevalue"])
                    
                    if teacherName == "":
                        teacherName = str(infos[9]["hidevalue"])

                    # 去除课程编号（[xxx001]）
                    courseName = courseName.split(']')[1]

                    courseInfo = {}

                    courseInfo["courseName"] = courseName
                    courseInfo["teacherName"] = teacherName
                    courseInfo["courseTime"] = courseTime
                    courseInfo["courseWeek"] = courseWeek
                    courseInfo["courseLocation"] = courseLocation
                    courseInfo["courseDetail"] = ""

                    coursesInfo.append(courseInfo)

                # 实验课
                elif len(infos) == 12:
                    courseName = str(infos[1].get_text())
                    if courseName == "":
                        courseName = str(infos[1]["hidevalue"])
                    courseDetail = str(infos[6].get_text())
                    teacherName = str(infos[7].get_text())
                    courseWeek = str(infos[9].get_text())
                    courseTime = str(infos[10].get_text())
                    courseLocation = str(infos[11].get_text())

                    # 去除课程编号（[xxx001]）
                    courseName = courseName.split(']')[1]

                    # 去除实验编号（[xxx001]）
                    courseDetail = courseDetail.split('-')[1][3:]

                    courseInfo = {}

                    courseInfo["courseName"] = courseName
                    courseInfo["teacherName"] = teacherName
                    courseInfo["courseTime"] = courseTime
                    courseInfo["courseWeek"] = courseWeek
                    courseInfo["courseLocation"] = courseLocation
                    courseInfo["courseDetail"] = courseDetail

                    coursesInfo.append(courseInfo)
    
    return coursesInfo

# 创建事件
def createEvent(dtStart, dtEnd, Summary, Location, Description):
    event = "BEGIN:VEVENT\r\n" + \
            "DTSTART;TZID=Asia/Shanghai:" + str(dtStart) + '\r\n' \
            "DTEND;TZID=Asia/Shanghai:" + str(dtEnd) + '\r\n' \
            "SUMMARY:" + str(Summary) + '\r\n' \
            "LOCATION:" + str(Location) + '\r\n' \
            "DESCRIPTION:" + str(Description) + '\r\n' \
            "END:VEVENT"
    return event

# 获取周几
# 将如 四[1-2节] 数据转换为数字返回
def changeDay(time):
    for i in range(0, len(weekdays)):
        if time[0] == weekdays[i]:
            return i

# 获取每节课周次
# 使用list存储所有周次
def changeWeek(week):
    # 处理形如1,2,3之类的数据
    week = week.split(',')

    weeks = []

    for w in week:
        # 处理形如1-2之类的数据
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

# 获取具体上下课时间
def changeTime(time):
    # 数据形如'四[1-2节]'，取出其中数据
    time = time[time.find('[') + 1:time.find(u'节')].split('-')

    # 只有一节，不存在，跳过
    if len(time) == 1:
        return 0, 0

    # 超出范围的课
    if int(time[0]) < 1 or int(time[1]) > 12:
        return 0, 0    
    
    # 取得开始、结束时间
    startTime = sTimes[int(time[0])]
    endTime = eTimes[int(time[1])]

    return startTime, endTime

# 创建日历文件
def MakeCalendar(courses, startDate):

    # 写入日历文件
    f = codecs.open("./courses.ics", "w", "utf-8")

    f.write("BEGIN:VCALENDAR\r\n")
    f.write("PRODID:-//Google Inc//Google Calendar 70.9054//EN\r\n")
    f.write("VERSION:2.0\r\n")
    f.write("CALSCALE:GREGORIAN\r\n")

    f.write("METHOD:PUBLISH\r\n")
    f.write("X-WR-CALNAME:classSchedule\r\n")
    f.write("X-WR-TIMEZONE:Asia/Shanghai\r\n")
    f.write("BEGIN:VTIMEZONE\r\n")
    f.write("TZID:Asia/Shanghai\r\n")
    f.write("BEGIN:STANDARD\r\n")
    f.write("TZOFFSETFROM:+0800\r\n")
    f.write("TZOFFSETTO:+0800\r\n")
    f.write("TZNAME:CST\r\n")
    f.write("DTSTART:19700101T000000\r\n")
    f.write("END:STANDARD\r\n")
    f.write("END:VTIMEZONE\r\n")

    for course in courses:

        weeks = changeWeek(course["courseWeek"])

        startTime, endTime = changeTime(course["courseTime"])

        # 异常课程跳过
        if startTime == endTime and startTime == 0:
            continue

        changeTime(course["courseTime"])
        for week in weeks:
            # 计算当前日期与第一周周一相隔天数
            days = (week - 1) * 7 + changeDay(course["courseTime"]) - 1
            # 使用datetime进行计算当前日期
            daysDelta = datetime.timedelta(days = days)
            nowDate = startDate + daysDelta

            dtStart = nowDate.strftime("%Y%m%d") + "T" + startTime
            dtEnd = nowDate.strftime("%Y%m%d") + "T" + endTime

            Description = course["teacherName"]
            if course["courseDetail"] != "":
                Description = Description + " " + course["courseDetail"]
            
            event = createEvent(dtStart, dtEnd, course["courseName"], course["courseLocation"], Description)

            f.write(event + '\r\n')
    
    f.write("END:VCALENDAR")
    f.close()

if __name__ == "__main__":
    startDate = datetime.datetime(startYear, startMonth, startDay)
    courses = ChangeCourse(GetOriginalCourse(username, password, executable_path, url))

    MakeCalendar(courses, startDate)

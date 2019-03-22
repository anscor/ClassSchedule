#!python3
# -*- coding: utf-8 -*-
'''
@Author: Anscor
@LastEditors: Anscor
@Description: 课程控制类
@Date: 2019-03-13
@LastEditTime: 2019-03-22
'''

import selenium
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import lxml
import hashlib
import json

import Config
from Formatter import Formatter
from Course import Course


class CourseControler:
    def __init__(self):
        self.user = Config.USER
        self.password = Config.PASSWORD
        self.exec_path = Config.EXEC_PATH
        self.jwc_url = Config.JWC_URL
        self.syjx_url = Config.SYJX_URL

    # 登录教务处网站，获取理论课程
    def __LoginJWC(self):
        option = Options()
        option.add_argument("--headless")
        option.add_argument("--disable-gpu")

        # 使用Chrome进行模拟点击
        driver = webdriver.Chrome(
            executable_path=self.exec_path,
            chrome_options=option)
        driver.get(self.jwc_url)

        # 登录
        driver.switch_to_frame("frmLogin")

        # 用户名和密码，即学号与密码
        usr = driver.find_element_by_id("txt_dsdsdsdjkjkjc")
        pwd = driver.find_element_by_id("txt_dsdfdfgfouyy")

        # 填入数据
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element(usr)
        action.send_keys(self.user)
        action.move_to_element(pwd)
        action.send_keys(self.password)
        action.move_to_element(usr)
        # 执行
        action.perform()

        # 登录按钮点击
        driver.find_element_by_class_name("but20").submit()

        return driver

    # 获取理论课网页
    def __GetOriginalTheoryCourse(self):
        driver = self.__LoginJWC()
        driver.get(self.jwc_url + "/znpk/Pri_StuSel.aspx")
        btn = driver.find_elements_by_class_name("button")
        btn[1].click()

        driver.switch_to_frame("frmRpt")

        # 取得课表页面网页内容
        originalCourse = driver.page_source

        driver.close()

        return originalCourse

    # 格式化理论课程，并返回一个 Course 类的List
    def __FormatTheoryCourse(self, originalCourse):
        bs = BeautifulSoup(originalCourse, "lxml")
        # 多页
        pages = bs.select(".content")

        courses = []

        for page in pages:
            courses = courses + self.__FormatTheoryPage(page)

        return courses

    # 格式化每页的理论课程，实验课程不处理
    def __FormatTheoryPage(self, page):
        # 课程信息表格
        tables = page.select(".page_table")

        courses = []

        for table in tables:
            # 过滤表头
            thead = table.select("thead")
            if len(thead) == 0:
                continue

            # 判断课程类型
            kind = len(thead[0].select("tr")[0].select("td"))

            # 实验课程跳过
            if kind == 11:
                continue

            tbody = table.select("tbody")

            table_items = tbody[0].select("tr")

            for item in table_items:
                infos = item.select("td")
                course = self.__FormatSingalTheoryCourse(infos)

                if course != None:
                    courses.append(course)
        return courses

    # 格式化单个理论课程
    def __FormatSingalTheoryCourse(self, infos):
        name = str(infos[1].get_text())
        teacher = str(infos[9].get_text())
        weeks = str(infos[10].get_text())
        time = str(infos[11].get_text())
        location = str(infos[12].get_text())

        # 同一课程，不同老师或不同时间教室不同等情况（如形式与政策课程等）
        if name == "":
            name = str(infos[1]["hidevalue"])

        if teacher == "":
            teacherName = str(infos[9]["hidevalue"])

        name = name.split(']')[1]

        # 格式化上课节次（对应到具体上、下课时间）、周次、天次（周几）
        formatter = Formatter()
        code, stime, etime = formatter.FormatTime(time)
        weeks = formatter.FormatWeek(weeks)
        day = formatter.FormatDay(time)

        # 某些特殊课程（如在13节）不处理，跳过
        if code == 0:
            course = Course(course=None, start_time=stime, end_time=etime, location=location,
                            teacher=teacher, name=name, detail="", weeks=weeks, day=day)
            return course
        else:
            return None

    # 登录实验教学网站，获取实验课程
    def __LoginSYJX(self):

        pwd = hashlib.md5(self.password.encode("utf-8")).hexdigest()

        data = {
            "username": self.user,
            "password": pwd
        }

        req = requests.post(self.syjx_url + "/login", data=data)
        return req.request.headers["Cookie"]

    # 获取实验课程Json
    def __GetOriginalEXPCourse(self):
        sess = self.__LoginSYJX()
        header = {
            "Cookie": sess,
            "Proxy-Connection": "keep-alive",
            "Content-Length": "0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "http://syjx.cqu.edu.cn",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Referer": "http://syjx.cqu.edu.cn/student/index",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
        }
        req = requests.post(
            self.syjx_url + "/student/schedule/query", headers=header)

        return req.text

    # 格式化实验课程，并返回一个 Course 类的List
    def __FormatEXPCourse(self, originalCourse):
        data = json.loads(originalCourse, encoding="utf-8")

        infos = data["booking"] + data["schedule"]

        formatter = Formatter()

        courses = []

        for info in infos:
            name = info["cn"]
            day = info["d"]
            code, stime, etime = formatter.FormatTime(info["ds"], 1)
            location = info["l"]
            detail = info["pn"]
            teacher = info["tn"]
            weeks = formatter.FormatWeek(info["w"])

            course = Course(course=None, start_time=stime, end_time=etime, location=location,
                            teacher=teacher, name=name, detail=detail, weeks=weeks, day=day)
            courses.append(course)
        
        return courses

    # 获取课程
    def GetCourse(self):
        # 获取理论课程
        originalCourse = self.__GetOriginalTheoryCourse()
        courses = self.__FormatTheoryCourse(originalCourse)
        # courses = []

        # 获取实验课程
        originalCourse = self.__GetOriginalEXPCourse()
        courses = courses + self.__FormatEXPCourse(originalCourse)

        return courses

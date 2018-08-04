# -*- coding: utf-8 -*-
import requests
import os
from selenium import webdriver
import re
from time import sleep
import json
import sys

"""
本项目分以下步骤完成：
1.程序登陆进入云课堂（已完成，已测试）
2.进入到文件树页面/课程页面，并保存页面为html（已完成，已测试）
3.通过正则得到控制程式所需的字段并保存为列表套列表(已完成，已测试)
4.根据得到的列表套列表设计遍历程式循环访问资源页下载资源（已完成，已测试）
5.对文件的名字和路径进行操作（和4合并为PART FOUR）（已完成，已测试单个，等待添加下载模式，只考虑了非媒体文件）
6.完成主函数（已完成，已测试）
"""


# ------ PART ONE ------
# 设置登陆函数
def star_c_login(account, password):
    headers = {
        'Origin': 'http://spoc.ccnu.edu.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://spoc.ccnu.edu.cn/starmoocHomepage',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = [
    ('loginName', account),
    ('password', password),
    ]

    session = requests.Session()

    resCheck = session.post('http://spoc.ccnu.edu.cn/userLoginController/checkLogin', headers=headers, data=data)
    # print(resCheck.text)
    dataload = json.loads(resCheck.text)
    if dataload['code'] == 0:
        print("登录成功!")
    elif dataload['code'] == 1:
        sys.exit("密码错误! 请重新登录")
    elif dataload['code'] == 2:
        sys.exit("用户名不存在!(学号错误)! 请重新登录")
    elif dataload['code'] == 99:
        sys.exit("用户验证失败！未知错误，请重新登录")
    else:
        print("未知登录状况，请谨慎后续操作。")

    resGup = session.post('http://spoc.ccnu.edu.cn/userLoginController/getUserProfile', headers=headers, data=data)
    # print('resGup.headers\n', resGup.headers)
    # print('resGup.requests.headers\n', resGup.request.headers)
    # print('resGup.text\n', resGup.text)
    # print('resGup.status_code\n', resGup.status_code)

    return session.cookies.get_dict()


# ------ PART TWO ------
# 通过输入的课程id，用requests方法得到json文件的html代码
def get_json_doc(siteID):
    data = [
    ('siteId', siteID),
    ]

    thisHeaders = {
        'Origin': 'http://spoc.ccnu.edu.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://spoc.ccnu.edu.cn/studentHomepage/studentCourseCenter?siteId=' + siteID,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    response = requests.post('http://spoc.ccnu.edu.cn/siteResource/getSiteResourceTree', headers=thisHeaders, cookies=resCookies, data=data)
    print(response.text)
    with open('getSiteResourceTree.json', 'w', encoding='utf-8') as f:
        f.write(response.text)



# ------ PART THREE ------
# 设置提取的pattern
"""
1.每个文件里有一个课程里的所有信息，且循环出现，所以我们进行三次findall就ok
2.警告：本函数目前仅尝试获取一个课程的信息，用于测试！！！
2.+若定义
"""

# 定义三个pattern 和一个pattern集
pattern1 = r'"attachmentInfoId":"(.*?)"'
pattern2 = r'"attachmentName":"(.*?)"'
pattern3 = r'"isMedia":"(0|1)"'
patterns = [pattern1, pattern2, pattern3]

# 定义一个结果集合
result = []
no_media = []


# 获取json文件里的信息
def get_all_info():
    global file_url
    global file_names
    global file_is_media
    with open('getSiteResourceTree.json', 'r', encoding='utf-8') as obj:
        single_course_info = obj.read()
        try:
            for i in range(3):
                pattern = patterns[i]
                result.append(re.findall(pattern, single_course_info, flags=re.S | re.I))
            print("提取成功")
            file_url = result[0]
            file_names = result[1]
            file_is_media = result[2]

            for s in range(len(file_url)):
                if str(file_is_media[s]) == '0':
                    no_media.append([file_url[s], file_names[s]])
                else:
                    continue

            # 打印结果
            print(file_url)
            print(file_names)
            print(file_is_media)
            print(no_media)
            return no_media

        except:
            print("提取失败，请重试")
            return ""


# ------ PART FOUR ------
# 设置访问资源站模式并将资源更名
def get_resource():
    # http://spoc.ccnu.edu.cn:80/getFileStream/ + 资源码
    driver = "C:/Users/HP/Desktop/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = driver  # 调用Chrome浏览器

    browser = webdriver.Chrome(driver)
    # 需要打开的网址
    try:
        for one in range(len(no_media)):
            browser.get('http://spoc.ccnu.edu.cn:80/getFileStream/' + str(no_media[one][0]))
            sleep(3)

            # 导入os方法
            # 对文件进行重命名
            """
            ---警示--- ：尚未考虑is_Media == 1时,此处仅下载了非视频文件
            """
            os.rename('C:/Users/HP/Downloads/' + str(no_media[one][0]) + '.xps',
                      'C:/Users/HP/Downloads/' + str(os.path.splitext(str(no_media[one][1]))[0]) + '.pdf')
            print("共有" + str(len(no_media)) + "个文件需要下载，已完成" + str(one + 1) + "个")

        print("ALL COMPLETED! ENJOY IT!")

    except OSError:
        print("学校服务器抽风了，请删除文件后重试！")


# 设置主函数
if __name__ == '__main__':
    # PART1
    print("---登陆---")
    account = input("请输入您的学号：\n")
    password = input("请输入您的密码：\n")
    resCookies = star_c_login(account, password)
    # PART2
    print("---获取资源---")
    siteID = input('输入您想要下载资源的网页 URL http://spoc.ccnu.edu.cn/studentHomepage/studentCourseCenter?siteId= 后面的字符串\n')
    get_json_doc(siteID)
    # PART3
    print("---去除媒体文件---")
    get_all_info()
    # PART4
    print("---下载中---")
    get_resource()

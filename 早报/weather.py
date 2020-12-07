# -*- coding: utf-8 -*-
# 规范第一行设置字符的编码格式 为UTF-8

# 导入正则模块 用来匹配想要的文字
import re
# 导入requests库，用requests库的get()方法来获取网页的源代码
import requests

# 这是要爬取的网页
url = "https://tianqi.moji.com/weather/china/anhui/tianjia'an-district"

# 使用response.get()方法获得这个网页的源代码
response = requests.get(url)

# 用正则表达式匹配规则从网页源代码里拿所需要的内容
weather = re.findall(r'<meta name="description" content="(.*?)">', response.text)[0]
print(weather)

# 将 墨迹天气 替换为你想要的名字
weather_robot = weather.replace('墨迹天气', '早报机器人')
print(weather_robot)

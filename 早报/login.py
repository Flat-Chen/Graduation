# -*- coding=utf-8 -*-
import requests
import time
from lxml import etree
from hex2b64 import HB64
import RSAJS


class Longin():
    def __init__(self, user, password):
        # 初始化程序数据
        self.Username = user
        self.Password = password
        nowTime = lambda: str(round(time.time() * 1000))
        self.now_time = nowTime()
        # 登录主页url
        self.login_url = "http://211.70.176.172/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t="
        # 请求PublicKey的URL
        self.login_Key = "http://211.70.176.172/jwglxt/xtgl/login_getPublicKey.html?time="

    def Get_indexHtml(self):
        # 获取教务系统网站
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": self.login_url + self.now_time,
            "Upgrade-Insecure-Requests": "1"
        })
        self.response = self.session.get(self.login_url + self.now_time).content.decode("utf-8")

    def Get_csrftoken(self):
        # 获取到csrftoken
        lxml = etree.HTML(self.response)
        self.csrftoken = lxml.xpath("//input[@id='csrftoken']/@value")[0]
        # print(self.csrftoken)

    def Get_PublicKey(self):
        # 获取到加密公钥
        key_html = self.session.get(self.login_Key + self.now_time)
        key_data = key_html.json()
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]
        # print(self.modulus)
        # print(self.exponent)

    def Get_RSA_Password(self):
        # 生成RSA加密密码
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus), HB64().b642hex(self.exponent))
        self.enPassword = HB64().hex2b64(rsaKey.encrypt(self.Password))
        # print(self.enPassword)

    def Longin_Home(self):
        # 登录信息门户,成功返回session对象
        self.Get_indexHtml()
        self.Get_csrftoken()
        self.Get_PublicKey()
        self.Get_RSA_Password()
        login_data = [("csrftoken", self.csrftoken), ("yhm", self.Username), ("mm", self.enPassword),
                      ("mm", self.enPassword)]
        login_html = self.session.post(self.login_url + self.now_time, data=login_data)
        # 当提交的表单是正确的，url会跳转到主页，所以此处根据url有没有跳转来判断是否登录成功
        if login_html.url.find("login_slogin.html") == -1:  # -1没找到，说明已经跳转到主页
            print("登录成功")
            # print(login_html.url)
            return self.session
        else:
            print("用户名或密码不正确，登录失败")
            exit()


class TimeTable():
    def __init__(self, session):
        # 登录后的课表URL
        table_url = "http://211.70.176.172/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"
        data = {"xnm": 2020, "xqm": 3}
        table_info = session.post(table_url, data=data).json()
        self.table_info = table_info
        for each in table_info["kbList"]:
            plt = r'{} | {} | {} | {} | {}'
            print(plt.format(each["xqjmc"], each["jc"], each["cdmc"], each["zcd"], each["kcmc"]))

    def get_class_schedule(self):
        class_schedule = {}
        for each in self.table_info["kbList"]:
            class_schedule[each["xqjmc"]] = {'节程': each["jc"], '教室': each["cdmc"], '课时': each["zcd"],
                                             '课程名称': each["kcmc"]}
        # print(class_schedule)
        return class_schedule


if __name__ == "__main__":
    zspt = Longin("1708010127", "193728abC")
    response_cookies = zspt.Longin_Home()
    table = TimeTable(response_cookies)

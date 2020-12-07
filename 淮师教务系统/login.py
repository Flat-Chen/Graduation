# -*- coding=utf-8 -*-
import requests
import time
from lxml import etree
from hex2b64 import HB64
import RSAJS


class Longin():

    def __init__(self, user, password, login_url, login_KeyUrl):
        # 初始化程序数据
        self.Username = user
        self.Password = password
        nowTime = lambda: str(round(time.time() * 1000))
        self.now_time = nowTime()

        self.login_url = login_url
        self.login_Key = login_KeyUrl

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
        print(self.csrftoken)

    def Get_PublicKey(self):
        # 获取到加密公钥
        key_html = self.session.get(self.login_Key + self.now_time)
        key_data = key_html.json()
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]
        print(self.modulus)
        print(self.exponent)

    def Get_RSA_Password(self):
        # 生成RSA加密密码
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus), HB64().b642hex(self.exponent))
        self.enPassword = HB64().hex2b64(rsaKey.encrypt(self.Password))
        print(self.enPassword)

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
            print(login_html.url)
            return self.session
        else:
            print("用户名或密码不正确，登录失败")
            exit()


class TimeTable():
    def __init__(self, session, table_url):
        data = {"xnm": 2020, "xqm": 3}
        table_info = session.post(table_url, data=data).json()
        # print(table_info)
        # print(table_info["kbList"])
        for each in table_info["kbList"]:
            plt = r'{} | {:<8s} | {:<12s} | {:<18s} | {:<29s}'
            print(plt.format(each["xqjmc"], each["jc"], each["cdmc"], each["zcd"], each["kcmc"]))

    def get_class_schedule(self):
        pass


if __name__ == "__main__":
    # 登录主页url
    login_url = "http://211.70.176.172/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t="
    # 请求PublicKey的URL
    login_KeyUrl = "http://211.70.176.172/jwglxt/xtgl/login_getPublicKey.html?time="
    # 登录后的课表URL
    table_url = "http://211.70.176.172/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"

    zspt = Longin("1708010127", "193728abC", login_url, login_KeyUrl)
    response_cookies = zspt.Longin_Home()
    table = TimeTable(response_cookies, table_url)

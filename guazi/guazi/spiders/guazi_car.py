# -*- coding: utf-8 -*-
# 导入本项目需要的库
import json
import time
import scrapy
from guazi.items import GuaziItem


# 定义一个爬虫类
class GuaziCarSpider(scrapy.Spider):
    # 爬虫名字
    name = 'guazi_car'
    # 爬虫只抓取这个域名下面的链接
    allowed_domains = ['guazi.com']
    # 爬虫的起始链接，这个连接时手机上抓到的车系大全
    start_urls = ['https://marketing.guazi.com/marketing/brand/haveTags/all?cityId=12&size=14']

    # 爬虫从parse开始往下执行解析页面
    def parse(self, response):
        # 创建一个data对象，将上面起始链接接口请求到的数据赋值给data
        data = response.text
        # 将接data从str文本格式转变为dict字典显示，也就是json格式
        json_data = json.loads(data)
        # 开始解析，从放在循环里面，一个一个的进行解析
        for i in json_data['data']['brands']:
            for brand in json_data['data']['brands'][i]:
                # print(brand)
                brand_id = brand['id']
                brandname = brand['name']
                for family in brand['tags']:
                    family_id = family['id']
                    familyname = family['name']
                    # print(brandname, brand_id, familyname, family_id)
                    # 品牌id抓完了，构建一个新的url为车型接口，
                    # 将上面得到的车系id传到下面url里的{family_id}里面，既可以得到这个车系里的每一款车型
                    url = f'https://api.guazi.com/clientUc/brand/type?seriesId={family_id}'
                    # 将这个构建好的url重新扔到请求队列，让下载器下载，下载完让callback后指定的方法去解析，
                    # meta是这个方法中的变量传入到随着这个url一起传入到下一个方法中
                    yield scrapy.Request(url=url, callback=self.vehicle_parse,
                                         meta={"info": (brand_id, brandname, family_id, familyname)})

    # 解析车系的方法
    def vehicle_parse(self, response):
        # 接收上面parse方法通过yield meta传来的变量
        brand_id, brandname, family_id, familyname = response.meta.get('info')
        # 实例化一个item item为之前定义的值 只接受原来定义好的要抓的字段
        item = GuaziItem()
        # 和上面同理解析
        data = response.text
        json_data = json.loads(data)
        for data in json_data['data']:
            years = data
            for value in json_data['data'][data]:
                vehicle_id = value['id']
                vehicle = value['name']
                transmission = value['bian_su_qi']
                emission_standard = value['pai_fang_biao_zhun']
                seats = value['seats']
                item['grab_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['brandname'] = brandname
                item['brand_id'] = brand_id
                item['familyname'] = familyname
                item['family_id'] = family_id
                item['vehicle'] = vehicle
                item['vehicle_id'] = vehicle_id
                item['years'] = years
                item['transmission'] = transmission
                item['emission_standard'] = emission_standard
                item['seats'] = seats
                item['url'] = response.url + str(vehicle_id)
                item['status'] = item['url'] + '-' + str(vehicle_id) + '-' + str(vehicle)
                # 将所抓到的字段都传给item，通过item格式化后使用pipeline里的方法进行相应的存储操作
                yield item

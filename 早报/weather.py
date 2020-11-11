import requests
from lxml import etree

url = "https://tianqi.moji.com/weather/china/anhui/tianjia'an-district"

response = requests.get(url)
html = etree.HTML(response.text)
today_weather = ''.join(html.xpath("//ul[@class = 'days clearfix'][1]//text()")) \
    .strip().replace(' ', '').replace('\n', ' ').replace('\r', '').split(' ')
today_weather = list(filter(None, today_weather))
print(today_weather)

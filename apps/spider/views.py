import requests

from bs4 import BeautifulSoup
from django.views import View
from django.contrib.auth.models import User

from spiders import LianjiaSecondHandSpider
from libs.response import json_response
from apps.visualization import models as v_models
from . import constants

# Create your views here.


class LianJiaCitySpiderView(View):
    """链家城市列表爬虫视图"""

    def get(self, request):
        """启动链家爬虫获取数据并入库"""
        url = "https://www.lianjia.com/city/"
        req = requests.get(url, headers=constants.HEADERS)
        soup = BeautifulSoup(req.text, "html.parser")
        tag_list = soup.select(".city_province ul li a")

        for item in tag_list:
            city_name = item.text
            href = item.get("href")
            user = User.objects.get(username="spider")

            v_models.CityModel.objects.get_or_create(city_name=city_name, subdomain=href, created_by=user)
        return json_response()


class LianJiaSecondHandSpiderView(View):
    """链家城市二手房信息入库视图"""

    def get(self, request):
        spider = LianjiaSecondHandSpider("深圳")
        res = spider.run()
        if not res:
            return json_response("请进行人机认证")
        for item in res:
            user = User.objects.get(username="spider")
            city = v_models.CityModel.objects.get(city_name=spider.city_name)
            item["created_by"] = user  # 设置用户外键
            item["city"] = city  # 设置城市外键

            house_obj = v_models.HouseInfoModel.objects.filter(house_code=item["house_code"])
            if house_obj:
                house_obj.update(**item)
                continue
            v_models.HouseInfoModel.objects.create(**item)

        return json_response()

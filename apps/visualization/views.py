import requests

from bs4 import BeautifulSoup
from django.views import View
from django.contrib.auth.models import User

from spiders import LianjiaSecondHandASyncSpider, LianjiaEstateSpider
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


class LianJiaDistrictSpiderView(View):
    """链家辖区入库视图"""
    def get(self, request):
        city_name = request.GET.get("city_name", "深圳")
        city_obj = v_models.CityModel.objects.get(city_name=city_name)
        subdomain = city_obj.subdomain
        start_url = f"{subdomain}ershoufang/"

        req = requests.get(start_url, headers=constants.HEADERS)
        soup = BeautifulSoup(req.text, "html.parser")
        tag_list = soup.select("div[data-role='ershoufang'] div a")  # 筛选出辖区 a 标签列表

        for tag in tag_list:  # 遍历所有辖区标签，访问并取得子级位置信息和对应 URL 入库
            district_model = v_models.DistrictModel(district_name=tag.text, city=city_obj)
            district_model.save()  # 创建一个辖区

            temp_url = tag.get("href")  # 获取该次遍历的辖区 URL
            req = requests.get(f"{start_url}{temp_url}", headers=constants.HEADERS)
            soup = BeautifulSoup(req.text, "html.parser")
            tag = soup.select("div[data-role='ershoufang'] div")[1]  # 筛选出子级列表的标签列表
            tag_location_list = tag.select("a")

            for item in tag_location_list:  # 遍历入库子级区域
                if v_models.DistrictModel.objects.filter(district_name=item.text):
                    continue
                location_model = v_models.DistrictModel(district_name=item.text, city=city_obj, parent=district_model)
                location_model.save()

        return json_response()


class LianJiaEstateSpiderView(View):
    """链家小区入库爬虫视图"""
    def get(self, request):
        city_name = self.request.GET.get("city_name", "深圳")
        spider = LianjiaEstateSpider(city_name)
        info_list = spider.get_all_estates()  # 获取所有小区信息

        for item in info_list:  # 遍历将数据入库
            district = v_models.DistrictModel.objects.get(district_name=item["house_district"])
            if v_models.EstateModel.objects.filter(house_code=item["house_code"]):
                continue
            estate = v_models.EstateModel(
                district=district, estate_name=item["title"], house_code=item["house_code"]
            )
            estate.save()

        return json_response()


class LianJiaSecondHandSpiderView(View):
    """链家城市二手房信息入库视图"""

    def get(self, request):
        spider = LianjiaSecondHandASyncSpider("深圳")
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

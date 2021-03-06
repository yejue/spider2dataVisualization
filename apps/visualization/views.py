import os
import requests
import logging

from bs4 import BeautifulSoup
from django.views import View
from django.contrib.auth.models import User

from spiders import LianjiaEstateSpider, LianjiaSecondHandSpider
from libs.response import json_response
from libs.baiduTools import BaiduMap
from apps.visualization import models as v_models
from . import constants

# Create your views here.

spider_logger = logging.getLogger("spider")
BAIDU_MAP_COORDS_AK = os.getenv("BAIDU_MAP_COORDS_AK")  # 百度地图经纬度 access_key


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
        spider_logger.info("链家城市入库爬虫爬行完毕")
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
            district = v_models.DistrictModel.objects.get_or_create(district_name=tag.text, city=city_obj)[0]
            temp_url = tag.get("href")  # 获取该次遍历的辖区 URL
            req = requests.get(f"{start_url}{temp_url}", headers=constants.HEADERS)
            soup = BeautifulSoup(req.text, "html.parser")
            tag = soup.select("div[data-role='ershoufang'] div")[1]  # 筛选出子级列表的标签列表
            tag_location_list = tag.select("a")

            for item in tag_location_list:  # 遍历入库子级区域
                if v_models.DistrictModel.objects.filter(district_name=item.text):
                    continue
                location_model = v_models.DistrictModel(district_name=item.text, city=city_obj, parent=district)
                location_model.save()
        spider_logger.info("链家辖区表入库爬虫爬行完毕")
        return json_response()


class LianJiaEstateSpiderView(View):
    """链家小区入库爬虫视图"""
    def get(self, request):
        city_name = self.request.GET.get("city_name", "深圳")
        spider = LianjiaEstateSpider(city_name)
        info_list = spider.get_all_estates()  # 获取所有小区信息

        for item in info_list:  # 遍历将数据入库
            district = v_models.DistrictModel.objects.get(district_name=item["district"])
            item["district"] = district

            if v_models.EstateModel.objects.filter(house_code=item["house_code"]):
                estate = v_models.EstateModel.objects.get(house_code=item["house_code"])
                estate.__dict__.update(**item)
                estate.save()
                continue
            estate = v_models.EstateModel(**item)
            estate.save()
        spider_logger.info("链家小区表入库爬虫爬行完毕")
        return json_response()


class LianJiaSecondHandSpiderView(View):
    """链家城市二手房信息入库视图"""

    def get(self, request):
        city_name = self.request.GET.get("city_name", "深圳")
        spider = LianjiaSecondHandSpider(city_name)
        res = spider.get_houses()

        if not res:
            return json_response("请进行人机认证")

        for info_list in res:
            for item in info_list:  # 从每一页的数据中遍历每一条目信息

                user = User.objects.get(username="spider")
                estate = v_models.EstateModel.objects.filter(estate_name=item["estate"]).first()

                item["created_by"] = user  # 设置用户外键
                item["estate"] = estate  # 设置城市外键

                house_obj = v_models.HouseInfoModel.objects.filter(house_code=item["house_code"])
                if house_obj:
                    house_obj.update(**item)
                    continue
                v_models.HouseInfoModel.objects.create(**item)
        spider_logger.info(f"链家{city_name}二手房数据爬虫爬行完毕")
        return json_response()


class EstateAddCoordinateView(View):
    """小区坐标入库视图
     - 用于获取小区表中条目地址对应的坐标，并更新对应条目
    """
    def get(self, request):
        access_key = BAIDU_MAP_COORDS_AK
        queryset = v_models.EstateModel.objects.filter(lon=None, lat=None)
        map_tool = BaiduMap(access_key)  # 百度地图工具

        for item in queryset:  # 遍历每一个条目，用其中地址获取坐标入库
            address = f"广东省{item.district.city.city_name}{item.district.district_name}{item.estate_name}"
            res = map_tool.get_coordinate_by_address(address)
            if res["status"] != 0:  # 状态不正常时跳过
                print(res)
                continue

            lon, lat = res["result"]["location"]["lng"], res["result"]["location"]["lat"]
            item.lon = lon
            item.lat = lat
            item.save()
        spider_logger.info("小区坐标更新成功")
        return json_response()


class DistrictAddCoordinateView(View):
    """辖区坐标获取与入库视图
     - 用于获取辖区表中条目地址对应的坐标，并更新对应条目
    """
    def get(self, request):
        access_key = BAIDU_MAP_COORDS_AK
        queryset = v_models.DistrictModel.objects.filter(lon=None, lat=None, parent__isnull=False)  # 去除行政区和有坐标的条目
        map_tool = BaiduMap(access_key)  # 百度地图工具

        for item in queryset:  # 遍历每一个条目，用其中地址获取坐标入库
            address = f"广东省{item.city.city_name}{item.parent.district_name}{item.district_name}"
            res = map_tool.get_coordinate_by_address(address)
            if res["status"] != 0:  # 状态不正常时跳过
                print(res)
                continue

            lon, lat = res["result"]["location"]["lng"], res["result"]["location"]["lat"]
            item.lon = lon
            item.lat = lat
            item.save()
        spider_logger.info("辖区坐标更新成功")
        return json_response()

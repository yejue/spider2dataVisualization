import os
import logging

from django.core.management.base import BaseCommand
from apps.visualization import models as v_models
from libs.baiduTools import BaiduMap


spider_logger = logging.getLogger("spider")
BAIDU_MAP_COORDS_AK = os.getenv("BAIDU_MAP_COORDS_AK")  # 百度地图经纬度 access_key


class Command(BaseCommand):

    def handle(self, *args, **options):
        """处理函数"""
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

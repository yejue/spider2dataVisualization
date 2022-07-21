import sys
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.visualization import models as v_models
from spiders import LianjiaEstateSpider


spider_logger = logging.getLogger("spider")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("city_name")  # 添加一个城市名字作为位置参数

    def handle(self, *args, **options):
        """处理函数"""
        argv = sys.argv
        city_name = argv[2]
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

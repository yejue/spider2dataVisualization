import sys
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.visualization.models import HouseInfoModel, CityModel
from spiders import LianjiaSecondHandSpider

spider_logger = logging.getLogger("spider")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("city_name")  # 添加一个城市名字作为位置参数

    def handle(self, *args, **options):
        """处理函数
          1.  启动异步爬虫，取得链家二手房数据，并入库
        """
        argv = sys.argv
        city_name = argv[2]
        spider = LianjiaSecondHandSpider(city_name)
        res = spider.run()

        if not res:
            return spider_logger.info("数据爬取失败，请进行人机验证")
        for item in res:
            user = User.objects.get(username="spider")
            item["created_by"] = user
            item["city"] = CityModel.objects.get(city_name=city_name)
            house_obj = HouseInfoModel.objects.filter(house_code=item["house_code"])
            if house_obj:
                house_obj.update(**item)
                continue
            HouseInfoModel.objects.create(**item)
        return spider_logger.info(f"{city_name}数据爬行完成")

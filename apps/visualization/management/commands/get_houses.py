import sys
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.visualization import models as v_models
from spiders import LianjiaSecondHandSpider

spider_logger = logging.getLogger("spider")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("city_name")  # 添加一个城市名字作为位置参数

    def handle(self, *args, **options):
        """处理函数
          1.  启动爬虫，取得链家二手房数据，并入库
        """
        argv = sys.argv
        city_name = argv[2]
        spider = LianjiaSecondHandSpider(city_name)
        res = spider.get_houses()

        if not res:
            spider_logger.info("请进行人机认证")
            return

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

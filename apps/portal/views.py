import json

from django.shortcuts import render
from django.views import View
from django.db.models import Avg

from apps.visualization import models
# Create your views here.


class IndexView(View):
    """首页视图"""
    def get(self, request):
        return render(self.request, "portal/index.html")


class HousingPriceDistributionView(View):
    """房价分布页视图

    渲染到前端的数据结构大概如下 data

    data = {
        "estate_list": [
            {"estate_name": "", "lon": float, "lat": float, "avg_price": float, "total_price": float},
        ],
        "total_price_top10": [
            {"house_name": "", "total_price": float},
        ],
        "unit_price_top10": [
            {"house_name": "", "unit_price": float},
        ],
    }

    """

    def get(self, request):
        estate_queryset = models.EstateModel.objects.all()
        estate_list = []  # 小区信息列表
        total_price_top10 = []  # 房子总价前10列表
        unit_price_top10 = []  # 房子每平米单价前10列表

        for item in estate_queryset:  # 序列化小区信息
            total_price_avg = models.HouseInfoModel.objects.filter(estate=item).aggregate(Avg("total_price"))
            temp = {
                "estate_name": item.estate_name,
                "lon": item.lon,
                "lat": item.lat,
                "avg_price": total_price_avg.get("total_price__avg")
            }
            estate_list.append(temp)

        for item in models.HouseInfoModel.objects.all().order_by("-total_price")[:10]:  # 序列化房子总价 top10 信息
            temp = {
                "house_name": f"{item.estate.estate_name}{item.house_area}平{item.house_type}",
                "house_type": item.house_type,
                "house_area": item.house_area,
                "total_price": item.total_price,
            }
            total_price_top10.append(temp)

        for item in models.HouseInfoModel.objects.all().order_by("-unit_price")[:10]:  # 序列化房子单价 top10 信息
            temp = {
                "house_name": f"{item.estate.estate_name}{item.house_area}平{item.house_type}",
                "house_type": item.house_type,
                "house_area": item.house_area,
                "unit_price": item.unit_price,
            }
            unit_price_top10.append(temp)

        distribution_data = {
            "estate_list": estate_list,
            "total_price_top10": total_price_top10,
            "unit_price_top10": unit_price_top10,
        }
        distribution_data = json.dumps(distribution_data, ensure_ascii=False)

        return render(self.request, "portal/distribution.html", context={"distribution_data": distribution_data})


class BigViewView(View):
    """大屏图表视图"""
    def get(self, request):
        return render(self.request, "portal/big_view.html")


class VideoListView(View):
    """可视化图表赛跑视频列表视图"""
    def get(self, request):
        return render(self.request, "portal/video_list.html")

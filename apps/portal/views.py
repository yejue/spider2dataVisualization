import json

from django.shortcuts import render
from django.views import View
from django.db.models import Count, Sum

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
        "total_price_top10": [
            {"house_name": "", "total_price": float},
        ],
        "unit_price_top10": [
            {"house_name": "", "unit_price": float},
        ],
    }

    heatmap_data = [
        {"coord": [120.14322240845, 30.236064370321], "elevation":21},
        {"coord": [120.14322240845, 30.236064370321], "elevation":21},
    ]

    """

    def get(self, request):
        estate_queryset = models.EstateModel.objects.all()
        heatmap_list = []  # 小区信息列表
        total_price_top10 = []  # 房子总价前10列表
        unit_price_top10 = []  # 房子每平米单价前10列表

        for item in estate_queryset:  # 序列化小区信息
            temp = {
                "coord": [item.lon, item.lat],
                "elevation": item.avg_price  # 本小区所有房子的平均价格
            }
            heatmap_list.append(temp)
        for item in models.HouseInfoModel.objects.all().order_by("-total_price")[:10]:  # 序列化房子总价 top10 信息
            temp = {
                "house_name": f"{item.estate.estate_name}{item.house_area}平{item.house_type}",
                "house_type": item.house_type,
                "house_area": item.house_area,
                "total_price": item.total_price,
            }
            total_price_top10.append(temp)

        for item in models.HouseInfoModel.objects.all().order_by("-unit_price")[:10]:  # 序列化房子单价 top10 信息

            if item.estate:
                estate_name = item.estate.estate_name
            else:
                estate_name = ""

            temp = {
                "house_name": f"{estate_name}{item.house_area}平{item.house_type}",
                "house_type": item.house_type,
                "house_area": item.house_area,
                "unit_price": item.unit_price,
            }
            unit_price_top10.append(temp)

        top10_data = {
            "total_price_top10": total_price_top10,
            "unit_price_top10": unit_price_top10,
        }
        top10_data = json.dumps(top10_data, ensure_ascii=False)

        return render(self.request, "portal/distribution.html", context={
            "top10_data": top10_data,
            "heatmap_data": json.dumps(heatmap_list),
        })


class BigViewView(View):
    """大屏图表视图"""
    def get(self, request):
        # 取得线性表 line-chart 的数据
        queryset = models.HouseInfoModel.objects.all().order_by("house_area")
        ft_queryset = queryset.filter(estate__district__parent__district_name="福田区").order_by("house_area")  # 筛选福田区的数据
        lg_queryset = queryset.filter(estate__district__parent__district_name="龙岗区").order_by("house_area")  # 筛选龙岗区的数据

        line_chart_data = {
            "area_list": [item.house_area for item in queryset],
            "price_list": [item.total_price for item in queryset],
        }

        ft_chart_data = {
            "area_list": [item.house_area for item in ft_queryset],
            "price_list": [item.total_price for item in ft_queryset],
        }

        lg_chart_data = {
            "area_list": [item.house_area for item in lg_queryset],
            "price_list": [item.total_price for item in lg_queryset],
        }

        # 取得饼图的数据
        pie_queryset = models.HouseInfoModel.objects.values("house_type")\
            .annotate(Count("house_type")).order_by("-house_type__count")
        pie_data = []
        sum_type = sum([item["house_type__count"] for item in pie_queryset])  # 所有条目的 count 总数
        cur_sum_type = 0  # 当前存起来的 count 数量

        for item in pie_queryset[:7]:  # 只取前 7 个 house_type
            cur_sum_type += item["house_type__count"]  # 记录总数
            temp = {"name": item["house_type"], "value": item["house_type__count"]}
            pie_data.append(temp)

        pie_data.append({"name": "其他", "value": sum_type-cur_sum_type})  # 除被选择的类型外，全部为其他类型

        return render(self.request, "portal/big_view.html", context={
            "line_chart_data": json.dumps(line_chart_data),
            "lg_chart_data": json.dumps(lg_chart_data),
            "ft_chart_data": json.dumps(ft_chart_data),
            "pie_data": json.dumps(pie_data),
        })


class VideoListView(View):
    """可视化图表赛跑视频列表视图"""
    def get(self, request):
        return render(self.request, "portal/video_list.html")

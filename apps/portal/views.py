import json

from django.shortcuts import render
from django.views import View
from django.db.models import Count, Avg

from apps.visualization import models
# Create your views here.


class IndexView(View):
    """首页视图"""
    def get(self, request):
        return render(self.request, "portal/index.html")


class HousingPriceDistributionView(View):
    """房价分布页视图

    渲染到前端的数据结构大概如下

    heatmap_data = [
        {"coord": [120.14322240845, 30.236064370321], "elevation":21},
        {"coord": [120.14322240845, 30.236064370321], "elevation":21},
    ]

    """

    def get(self, request):
        # 序列化热力图相关数据
        estate_queryset = models.EstateModel.objects.all()
        heatmap_list = []  # 小区信息列表

        for item in estate_queryset:  # 序列化小区信息
            temp = {
                "coord": [item.lon, item.lat],
                "elevation": item.avg_price  # 本小区房子的平均价格(当前使用的是参考均价)
            }
            heatmap_list.append(temp)

        # 取得房子总价 top10 相关的条目数据
        top10_queryset = models.HouseInfoModel.objects.all().order_by("-total_price")[:10]
        top10_convert = []  # convert 之后的格式

        for item in top10_queryset:
            if item.estate:  # 有小区的房子正常添加
                estate = item.estate.estate_name
                top10_convert.append({
                    "name": estate,
                    "value": [
                        item.estate.lon, item.estate.lat, item.total_price, item.title, item.house_type, item.house_area
                    ]
                })
            else:
                estate = item.title  # 没有小区的使用 title 替代小区名字
                top10_convert.append({
                    "name": estate,
                    "value": [
                        None, None, item.total_price, item.title, item.house_type, item.house_area
                    ]
                })

        return render(self.request, "portal/distribution.html", context={
            "heatmap_data": json.dumps(heatmap_list),
            "top10_convert": json.dumps(top10_convert),
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

        # 取得地图数据：各区房价均值，其中龙岗和大鹏新区同属于龙岗区
        map_queryset = models.HouseInfoModel.objects\
            .values("estate__district__parent__district_name")\
            .annotate(avg_price=Avg("total_price"))\
            .order_by("-avg_price")

        map_data = []
        lg_list = []  # 龙岗区和大鹏新区 item 列表

        for item in map_queryset:
            if not item["estate__district__parent__district_name"]:  # 跳过没有小区的房子
                continue
            if item["estate__district__parent__district_name"] in ["龙岗区", "大鹏新区"]:  # 不在循环处理这两个区
                lg_list.append(item)
                continue
            map_data.append(
                {"name": item["estate__district__parent__district_name"], "value": "{:.3f}".format(item["avg_price"])}
            )

        # 将龙岗区和大鹏新区合成为龙岗区
        avg_price = sum([item["avg_price"] for item in lg_list]) / len(lg_list)
        map_data.append({"name": "龙岗区", "value": "{:.3f}".format(avg_price)})

        return render(self.request, "portal/big_view.html", context={
            "line_chart_data": json.dumps(line_chart_data),
            "lg_chart_data": json.dumps(lg_chart_data),
            "ft_chart_data": json.dumps(ft_chart_data),
            "pie_data": json.dumps(pie_data),
            "map_data": json.dumps(map_data),
        })


class VideoListView(View):
    """可视化图表赛跑视频列表视图"""
    def get(self, request):
        return render(self.request, "portal/video_list.html")

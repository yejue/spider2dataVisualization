from django.shortcuts import render
from django.views import View
# Create your views here.


class IndexView(View):
    """首页视图"""
    def get(self, request):
        return render(self.request, "portal/index.html")


class HousingPriceDistributionView(View):
    """房价分布页视图"""
    def get(self, request):
        return render(self.request, "portal/distribution.html")


class BigViewView(View):
    """大屏图表视图"""
    def get(self, request):
        return render(self.request, "portal/big_view.html")


class VideoListView(View):
    """可视化图表赛跑视频列表视图"""
    def get(self, request):
        return render(self.request, "portal/video_list.html")

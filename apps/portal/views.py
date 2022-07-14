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

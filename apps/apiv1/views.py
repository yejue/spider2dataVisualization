from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from apps.visualization.models import CityModel, HouseInfoModel, DistrictModel, EstateModel
from apps.apiv1 import serializers
# Create your views here.


class CustomPager(PageNumberPagination):
    """客制化分页器，默认一个页面至多展示50条"""
    page_size = 50
    page_query_param = 'page'
    max_page_size = 50


class CityViewSet(viewsets.ModelViewSet):
    """城市表视图集"""
    serializer_class = serializers.CityModelSerializer
    queryset = CityModel.objects.all()
    pagination_class = CustomPager


class HouseInfoViewSet(viewsets.ModelViewSet):
    """房子信息表视图集"""
    queryset = HouseInfoModel.objects.all()
    serializer_class = serializers.HouseInfoModelSerializer
    pagination_class = CustomPager


class DistrictViewSet(viewsets.ModelViewSet):
    """辖区表视图集"""
    queryset = DistrictModel.objects.all()
    serializer_class = serializers.DistrictModelSerializer
    pagination_class = CustomPager


class EstateViewSet(viewsets.ModelViewSet):
    """小区表"""
    queryset = EstateModel.objects.all()
    serializer_class = serializers.EstateModelSerializer
    pagination_class = CustomPager


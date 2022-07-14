from rest_framework import serializers
from apps.visualization.models import CityModel, HouseInfoModel, DistrictModel, EstateModel


class CityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = '__all__'


class HouseInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseInfoModel
        fields = '__all__'


class DistrictModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictModel
        fields = '__all__'


class EstateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateModel
        fields = '__all__'

from django.db import models
from django.contrib.auth.models import User
from libs.models import BaseModel
# Create your models here.


class CityModel(BaseModel):
    """城市表"""
    city_name = models.CharField("城市名字", max_length=32, unique=True, help_text="城市名字")
    subdomain = models.URLField("子域名链接", max_length=128, help_text="子域名链接")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"<id: {self.id} city_name: {self.city_name}>"

    class Meta:
        db_table = "city"
        ordering = ["id"]
        verbose_name = "城市表"
        verbose_name_plural = verbose_name


class DistrictModel(BaseModel):
    """辖区表"""
    city = models.ForeignKey(CityModel, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

    district_name = models.CharField("辖区名", max_length=128, help_text="辖区或者是某区域", unique=True)
    lon = models.FloatField("经度", null=True, help_text="经度")
    lat = models.FloatField("纬度", null=True, help_text="纬度")

    def __str__(self):
        return f"<id: {self.id} district_id: {self.district_name}>"

    class Meta:
        db_table = "district"
        ordering = ["id"]
        verbose_name = "辖区表"
        verbose_name_plural = verbose_name


class EstateModel(BaseModel):
    """小区表"""
    district = models.ForeignKey(DistrictModel, null=True, on_delete=models.SET_NULL)
    estate_name = models.CharField("小区名", max_length=128, help_text="小区名")
    lon = models.FloatField("经度", null=True, help_text="经度")
    lat = models.FloatField("纬度", null=True, help_text="纬度")
    house_code = models.CharField("房子编号", max_length=32, unique=True, help_text="房子编号", null=True)

    def __str__(self):
        return f"<id: {self.id} district: {self.estate_name}>"

    class Meta:
        db_table = "estate"
        ordering = ["id"]
        verbose_name = "小区表"
        verbose_name_plural = verbose_name


class HouseInfoModel(BaseModel):
    """房子信息表"""
    title = models.CharField("房子标题", max_length=256, help_text="房子标题")
    house_code = models.CharField("房子编号", max_length=32, unique=True, help_text="房子编号")
    location = models.CharField("位置", max_length=128, help_text="大概的位置，最低层次的位置信息")
    house_type = models.CharField("户型", max_length=32, help_text="户型")
    house_area = models.FloatField("房子面积", help_text="房子面积")
    total_price = models.FloatField("总价", help_text="总价")
    unit_price = models.FloatField("单价", help_text="每单位价格")

    district = models.ForeignKey(DistrictModel, null=True, on_delete=models.SET_NULL)
    estate = models.ForeignKey(EstateModel, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"[{self.house_code}]{self.estate}——{self.title}>"

    class Meta:
        db_table = "house_info"
        ordering = ["id"]
        verbose_name = "房子信息表"
        verbose_name_plural = verbose_name

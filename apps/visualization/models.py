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


class HouseInfoModel(BaseModel):
    """房子信息表"""
    title = models.CharField("房子标题", max_length=256, help_text="房子标题")
    house_code = models.CharField("房子编号", max_length=32, unique=True, help_text="房子编号")
    estate = models.CharField("小区名", max_length=32, help_text="小区名")
    location = models.CharField("位置", max_length=128, help_text="位置")
    house_type = models.CharField("户型", max_length=32, help_text="户型")
    house_area = models.FloatField("房子面积", help_text="房子面积")
    total_price = models.FloatField("总价")
    unit_price = models.FloatField("单价")

    city = models.ForeignKey(CityModel, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"[{self.house_code}]{self.estate}——{self.title}>"

    class Meta:
        db_table = "house_info"
        ordering = ["id"]
        verbose_name = "房子信息表"
        verbose_name_plural = verbose_name

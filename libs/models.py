from django.db import models


class BaseModel(models.Model):
    """基础映射模型"""

    create_time = models.DateTimeField("创建时间", auto_now_add=True, help_text="创建时间")
    update_time = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    remarks = models.CharField("备注", max_length=128, null=True)

    class Meta:
        abstract = True

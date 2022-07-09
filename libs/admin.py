from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """基础管理类"""
    list_per_page = 10  # 每页默认展示 13 条数据

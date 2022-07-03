from django.views import View
from django.db.models import Model
from django.urls import path
from django.core.paginator import Paginator
from requests.exceptions import ConnectionError

from libs.response import json_response
from libs.res_code import Code, error_map


class SearchEngineSpiderView(View):
    """搜索引擎爬虫抽象视图"""
    spider_class = None

    def get(self, request):
        if not self.spider_class:
            raise ValueError("未指定爬虫类")
        key = request.GET.get("key")
        try:
            page_count = int(request.GET.get("page_count", 10))
        except ValueError as e:
            return json_response(result_code=Code.PARAM_ERR, message=f"{error_map[Code.PARAM_ERR]} {e}")

        try:
            spider = self.spider_class(key, page_count=page_count)
        except ConnectionError as e:
            return json_response(result_code=Code.CONNECT_ERR, message=f"{error_map[Code.CONNECT_ERR]} {e}")

        res = spider.run()

        data = res
        return json_response(data=data)


class SimpleAPIViewRoot(View):
    """API 基础视图类
     - 主要用于提供简单的序列化器和过滤器
    """
    operation_fields = []  # 需要操控的数据表字段
    model = Model  # 需要操控的数据表模型
    params_map = {}  # URL 参数与其数据类型对照表。{"key": "int/float/string"}
    paginate_by = 25  # 默认分页，每页显示的条目数量

    def get_model(self):
        """设置模型类"""
        if not hasattr(self, "model"):
            raise ValueError("未设置表模型")
        if isinstance(self.model, Model):
            raise TypeError("模型类型设置错误")
        return self.model

    def filter(self, queryset):
        """字段过滤器
         - 传入一个 queryset，过滤要操作的字段
        """
        filter_dict = {}
        for field in self.operation_fields:
            temp = self.request.GET.get(field)
            if temp:
                filter_dict.update({field: temp})

        queryset = queryset.filter(**filter_dict)
        return queryset

    def serialize(self, queryset):
        """简易序列化
         - 将 queryset 查询集重新格式化为 RESTFul 风格的数据列表
        """
        data = []

        for item in queryset:
            temp = {}
            for field in self.operation_fields:
                if field is None:
                    continue
                temp.update({field: item.__dict__[field]})
            data.append(temp)
        return data

    def get_url_params(self, request, raw=False):
        """URL 参数获取器
         - 可根据 params_map 自动检测或转换其类型
         - 可根据 raw 来取消其自动转换和检测
        """
        params_dict = {}
        if not self.params_map or not isinstance(self.params_map, dict):
            raise ValueError("未设置或未正常设置参数映射字典")
        for key in self.params_map.keys():
            value = request.GET.get(key, None)

            if not value:  # 当参数为空或为空格的时候不响应操作
                continue

            if raw:
                params_dict.update({key: value})
                continue

            try:
                if self.params_map[key] == "int":
                    value = int(value)
                if self.params_map[key] == "float":
                    value = float(value)
                if self.params_map[key] == "string":
                    pass
            except ValueError:  # 当参数类型不正确时，不对该参数进行响应
                continue
            params_dict.update({key: value})
        return params_dict


class SimpleAPIView(SimpleAPIViewRoot):
    """简易 API 视图
     - 自动序列化
     - 自动字段过滤
     - 自动分页过滤
     - 自动响应 GET 请求auth_user_user_permissions
    """
    params_map = {"page": "int", "limit": "int"}

    def get(self, request):
        queryset = self.model.objects.all()
        queryset = self.filter(queryset)
        data = self.serialize(queryset)

        page = self.get_url_params(request).get("page", 1)  # 可接收页数参数
        limit = self.get_url_params(request).get("limit", self.paginate_by)  # 可接收每页数量参数
        # 分页
        paginator_obj = Paginator(data, limit)
        page_data = list(paginator_obj.get_page(page))

        total_count = len(data)
        return json_response(data=page_data, total_count=total_count)


class SimpleAPIViewWithID(SimpleAPIViewRoot, View):
    """
    定制化 APIView 组件2
     - 对 id 路由进行响应
     - 提供改、查、删数据库接口
    """
    def get(self, request, pk):
        queryset = self.model.objects.filter(id=pk)
        data = self.serialize(queryset)
        return json_response(data=data)


class SimpleViewSet(SimpleAPIViewRoot):
    """简单视图集"""

    simple_api_view = SimpleAPIView
    simple_api_view_with_id = SimpleAPIViewWithID
    base_name = str

    def __init__(self, *args):
        super().__init__()
        # 初始化生成两种视图, 以备 get_urls 正常使用
        self.simple_api_view = self.generic_view(SimpleAPIView, "SimpleAPIViewShadow")
        self.simple_api_view_with_id = self.generic_view(SimpleAPIViewWithID, "SimpleAPIViewWithIDShadow")

    def get_urls(self):
        """返回所需 urlpatterns"""
        urlpatterns = [
            path(f"{self.base_name}/", self.simple_api_view.as_view(), name=f"{self.base_name}_list"),
            path(
                f"{self.base_name}/<int:pk>/",
                self.simple_api_view_with_id.as_view(),
                name=f"{self.base_name}_detail"
            ),
        ]
        return urlpatterns

    def generic_view(self, view, view_name):
        """生成 view 类"""
        model = self.get_model()
        fields = self.operation_fields
        cls = type(view_name, (view, ), dict(model=model, operation_fields=fields))
        return cls

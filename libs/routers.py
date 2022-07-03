class SimpleRouter:
    """简单路由生成器"""

    register_list = []

    def register(self, viewset):
        """将 viewset 注册
         - 将一个 viewset 视图集对象加入到列表
        """
        self.register_list.append(viewset)
        return self.register_list

    def get_urls(self):
        """生成所有注册的 urlpatterns
         - 遍历注册列表的 viewset 对象，返回一个 urlpatterns
        """
        urlpatterns = []
        for item in self.register_list:
            urlpatterns.extend(item().get_urls())
        return urlpatterns

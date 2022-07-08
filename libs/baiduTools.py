import requests


class BaiduMap:
    """百度地图类工具"""

    def __init__(self, key_word):
        self.key_word = key_word

    # def get_coordinate(self):
    #     res_json = baidu_get_lal(self.key_word)
    #     return res_json

    @staticmethod
    def baidu_get_lal(key_word):
        """
        lal = 经纬度英文的缩写 Latitude and longitude
        ak = 用户申请注册的key 这里我的key是sTKqcYLcHuVPZ0DPWz7HAGOuk9EP8rfe
        addresss = 地址关键词，经过少数几次测试，支持模糊搜索，例如输入大益村，会给我返回深圳大益村的经纬度

        """
        url = 'https://api.map.baidu.com/geocoding/v3/?address='+key_word+'+&output=json&ak' \
                                                                          '=sTKqcYLcHuVPZ0DPWz7HAGOuk9EP8rfe&callback' \
                                                                          '=showLocation '
        req = requests.get(url)
        # req.json()['result']['location']
        return req.json()


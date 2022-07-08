import requests


class BaiduMap:
    """百度地图类工具"""

    def __init__(self, key_word, lng, lat):
        self.key_word = key_word
        self.lng = lng
        self.lat = lat
    # def get_coordinate(self):
    #     res_json = baidu_get_lal(self.key_word)
    #     return res_json

    def get_coordinate_by_address(self):
        """
        lal = 经纬度英文的缩写 Latitude and longitude
        ak = 用户申请注册的key 这里我的key是sTKqcYLcHuVPZ0DPWz7HAGOuk9EP8rfe
        addresss = 地址关键词，经过少数几次测试，支持模糊搜索，例如输入大益村，会给我返回深圳大益村的经纬度

        """
        url = 'https://api.map.baidu.com/geocoding/v3/?address='+self.key_word+'&output=json&ak=sTKqcYLcHuVPZ0DPWz7HAGOuk9EP8rfe&callback=showLocation '
        req = requests.get(url)
        # req.json()['result']['location']
        return req.json()

    def get_address_by_coordinate(self):
        url = 'https://api.map.baidu.com/reverse_geocoding/v3/?ak=sTKqcYLcHuVPZ0DPWz7HAGOuk9EP8rfe&output=json' \
              '&coordtype=wgs84ll&location={:.8},{:.8}&qq-pf-to=pcqq.group&coordtype=bd09ll'.format(self.lat, self.lng)
        print(url)
        req = requests.get(url)
        return req.json()

def test():
    a = input()
    while a != 0:
        print(BaiduMap(key_word=a, lng=None, lat=None).get_coordinate_by_address())
        print(BaiduMap(key_word=a,
                       lng=BaiduMap(key_word=a, lng=None, lat=None).get_coordinate_by_address()['result']['location']['lng'],
                       lat=BaiduMap(key_word=a, lng=None, lat=None).get_coordinate_by_address()['result']['location']['lat']).get_address_by_coordinate()
          )
        a = input()

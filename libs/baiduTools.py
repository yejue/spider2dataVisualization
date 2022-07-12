import requests


class BaiduMap:
    """百度地图类工具"""

    def __init__(self, ak):
        self.ak = ak

    def get_coordinate_by_address(self, keyword):
        """通过地址获取坐标"""

        url = f'https://api.map.baidu.com/geocoding/v3/?address=' \
              f'{keyword}&output=json&ak={self.ak}&callback=showLocation '

        req = requests.get(url)
        return req.json()

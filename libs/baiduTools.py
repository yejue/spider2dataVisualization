import requests


class BaiduMap:
    """百度地图类工具"""

    def __init__(self):
        self.ak = "sTKqcYLcHuVPZ0DPWz7HAGOuk9EP8rfe"

    def get_coordinate_by_address(self, keyword):
        """通过地址获取坐标"""

        url = f'https://api.map.baidu.com/geocoding/v3/?address=' \
              f'{keyword}&output=json&ak={self.ak}&callback=showLocation '

        req = requests.get(url)
        return req.json()


if __name__ == '__main__':
    address = "广东省深圳市阳光绿地家园"
    map_tool = BaiduMap()

    coordinate = map_tool.get_coordinate_by_address(address)
    print(coordinate)

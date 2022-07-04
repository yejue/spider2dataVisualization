import json
import re
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from . import constants


class LianjiaSecondHandSpider:
    """链家二手房爬虫"""

    def __init__(self, city_name):
        self.subdomain = constants.SUB_DOMAIN_DICT  # 链家城市子域名链接字典
        self.headers = constants.HEADERS
        self.city_name = city_name

    def get_all_urls(self):
        """获取对应城市二手房所有页面链接"""
        start_url = f"{self.subdomain[self.city_name]}/ershoufang/"
        req = requests.get(start_url, headers=self.headers)
        soup = BeautifulSoup(req.text, "html.parser")

        if "人机" in soup.select_one("title").text:
            return False

        page_tag = soup.select_one(".page-box.house-lst-page-box").get("page-data")  # 获取页数标签对象
        page_dict = json.loads(page_tag)

        url_list = [start_url+f"pg{i}" for i in range(1, page_dict["totalPage"]+1)]  # 组合 URL 列表
        return url_list

    @staticmethod
    def parse_one_page(text):
        """解析一页内容"""
        soup = BeautifulSoup(text, "html.parser")
        info_list = soup.select(".info.clear")

        house_list = []  # 存放当前页面全部房子信息
        for item in info_list:  # 遍历解析当前页的全部数据
            title = item.select_one(".title a").text  # 标题
            house_code = item.select_one(".title a").get("data-housecode")  # 房子代码
            estate = item.select(".positionInfo a")[0].text  # 小区
            location = item.select(".positionInfo a")[1].text  # 大致位置

            house_info = item.select_one(".houseInfo").text.split("|")  # 房子信息文本列表
            house_type = house_info[0].strip()  # 户型
            house_area = float(re.findall(r'\d+\.\d+|\d+', house_info[1])[0])  # 房子面积

            total_price = float(item.select_one(".totalPrice.totalPrice2 span").text.strip())  # 房子总价
            unit_price = float(re.findall(r"\d+", item.select_one(".unitPrice span").text.replace(",", ""))[0])  # 每单位价格

            temp = {
                "title": title,
                "house_code": house_code,
                "estate": estate,
                "location": location,
                "house_type": house_type,
                "house_area": house_area,
                "total_price": total_price,
                "unit_price": unit_price
            }
            house_list.append(temp)
        return house_list

    async def get_one_page(self, url, sem):
        """异步获取一页的内容"""
        async with sem:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as resp:
                    res = await resp.text()  # 异步等待链家响应，取得页面文本数据
                    data = self.parse_one_page(res)
        return data

    async def get_all_pages(self):
        """异步获取所有页面信息"""
        semaphore = asyncio.Semaphore(constants.MAX_SEMAPHORE)  # 最大可开启异步线程
        task_list = []

        url_list = self.get_all_urls()
        if not url_list:
            print(f"[INFO] 请进行人机认证 {self.subdomain[self.city_name]}")
            return None
        for u in url_list:  # 遍历创建异步任务
            task = asyncio.create_task(self.get_one_page(u, semaphore))
            task_list.append(task)

        done, _ = await asyncio.wait(task_list)  # 等待异步任务结果
        res_list = []

        for d in done:  # 取出所有任务结果
            res_list.extend(d.result())

        return res_list

    def run(self):
        """启动链家二手房异步爬虫"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(self.get_all_pages())
        loop.close()
        return res

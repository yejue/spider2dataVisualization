import re
import json
import time

import requests
import asyncio
import aiohttp

from random import randint
from bs4 import BeautifulSoup
from . import constants


class LianjiaSpiderAbstract:
    """链家爬虫抽象类"""
    city_name = None
    headers = None
    subdomain = None  # 城市子域名

    def get_all_urls_by_location(self, start_url):
        """获取通过区域筛选信息的最小单位的初始页面 URL"""
        req = requests.get(start_url, headers=self.headers)
        soup = BeautifulSoup(req.text, "html.parser")
        tag_list = soup.select("div[data-role='ershoufang'] div a")  # 筛选出辖区 a 标签列表
        district_urls = []  # 辖区 URL 列表

        for item in tag_list:  # 遍历取出用辖区作为筛选条件的 URL 列表，添加到辖区 URL列表
            district_urls.append(f"{self.subdomain}{item.get('href')}")

        location_urls = []  # 使用位置筛选的 URL 列表，即链家位置筛选的最小单位筛选

        for d_url in district_urls:  # 遍历所有辖区初始链接，取得最小单位的开始的初始链接
            req = requests.get(d_url, headers=self.headers)
            soup = BeautifulSoup(req.text, "html.parser")
            tag = soup.select("div[data-role='ershoufang'] div")[1]
            tag_list = tag.select("a")

            for item in tag_list:
                location_urls.append(f"{self.subdomain}{item.get('href')}")

        return location_urls

    def get_page_urls(self, start_url):
        """通过初始页 URL 获取所有分页 URL"""
        # 1. 取得最大页数
        # 2. 根据链家的路由设计计算 URL
        req = requests.get(start_url, headers=self.headers)
        soup = BeautifulSoup(req.text, "html.parser")

        if "人机" in soup.select_one("title").text:
            return False

        page_tag = soup.select_one(".page-box.house-lst-page-box").get("page-data")  # 获取页数标签对象
        page_dict = json.loads(page_tag)

        url_list = [start_url + f"pg{i}" for i in range(1, page_dict["totalPage"] + 1)]  # 组合 URL 列表
        return url_list

    @staticmethod
    def parse_one_page(text):
        """解析一页的内容"""
        soup = BeautifulSoup(text, "html.parser")
        info_list = soup.select(".info.clear")

        house_list = []  # 存放当前页面全部房子信息
        for item in info_list:  # 遍历解析当前页的全部数据
            title = item.select_one(".title a").text  # 标题

            house_code = item.select_one(".title a").get("data-housecode")  # 房子代码
            if not house_code:  # 如果为空，则使用第二个参数获取 house_code
                house_code = item.select_one(".title a").get("data-lj_action_housedel_id")

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


class LianjiaSecondHandSpider(LianjiaSpiderAbstract):
    """链家二手房爬虫"""
    def __init__(self, city_name):
        self.city_name = city_name
        self.headers = constants.HEADERS
        self.subdomain = constants.SUB_DOMAIN_DICT[self.city_name]  # 获取对应城市的子域名

    def get_urls(self):
        """获取所有爬行需要的 URL"""
        start_url = f"{self.subdomain}ershoufang"
        url_list = self.get_all_urls_by_location(start_url)
        res_list = []
        for url in url_list:  # 通过每个位置 URL 初始页计算出该位置选项下所有的页面 URL
            page_list = self.get_page_urls(url)
            res_list.extend(page_list)
        return res_list

    def get_houses(self):
        """获取所有二手房信息"""
        url_list = self.get_urls()

        for url in url_list:
            req = requests.get(url, headers=self.headers)
            temp_list = self.parse_one_page(req.text)  # 获取每一页解析出来的结果
            time.sleep(randint(1, 10) / 10)  # 随机休眠 0.1 ~ 1 秒
            print(f"[INFO] 正在爬行: {url}, 获取到数量：{len(temp_list)}")
            yield temp_list


class LianjiaEstateSpider(LianjiaSpiderAbstract):
    """链家小区爬虫"""

    def __init__(self, city_name):
        self.city_name = city_name
        self.headers = constants.HEADERS
        self.subdomain = constants.SUB_DOMAIN_DICT[self.city_name]  # 获取对应城市的子域名

    @staticmethod
    def parse_one_page(text):
        """解析一页内容"""
        soup = BeautifulSoup(text, "html.parser")
        info_list = soup.select(".clear.xiaoquListItem")

        estate_list = []  # 存放当前页面全部小区信息
        for item in info_list:  # 遍历解析当前页的全部数据
            title = item.select_one(".title a").text  # 标题
            house_code = item.get("data-housecode")  # 房子代码
            house_district = item.select_one(".bizcircle").text  # 商圈或地区
            try:
                avg_price = float(item.select_one(".totalPrice span").text)  # 参考均价，无参考价则为 None
            except ValueError:
                avg_price = None

            temp = {
                "estate_name": title,
                "house_code": house_code,
                "district": house_district,
                "avg_price": avg_price,
            }
            estate_list.append(temp)
        return estate_list

    def get_urls(self):
        """获取所有爬行需要的 URL"""
        start_url = f"{self.subdomain}xiaoqu"
        url_list = self.get_all_urls_by_location(start_url)
        return url_list

    def get_all_estates(self):
        """获取所有小区信息"""
        url_list = self.get_urls()
        info_list = []  # 存放所有的小区信息

        for url in url_list:  # 遍历最小单位的初始 URL
            page_urls = self.get_page_urls(url)
            print(f"[INFO] 正在爬行：{url}")
            for p_url in page_urls:
                req = requests.get(p_url, headers=self.headers)
                temp_list = self.parse_one_page(req.text)  # 解析出每一页的内容
                info_list.extend(temp_list)
        return info_list


class LianjiaSecondHandASyncSpider(LianjiaSpiderAbstract):
    """链家二手房异步爬虫"""

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

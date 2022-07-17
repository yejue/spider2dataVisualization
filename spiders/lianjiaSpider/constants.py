import json
from pathlib import Path

# 当前文件位置
BASE_DIR = Path(__file__).resolve().parent

# 链家 HEADERS
HEADERS = {
    "Cookie": "lianjia_uuid=2c0786fe-c0de-4e1b-937a-b75f6cb8c046; _smt_uid=62bd06c9.c24e22f; _ga=GA1.2.1506927656.1656555213; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22181b262862f17-090f574dec1b89-978183a-1327104-181b2628630153%22%2C%22%24device_id%22%3A%22181b262862f17-090f574dec1b89-978183a-1327104-181b2628630153%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wybeijing%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; _jzqx=1.1656860786.1657601081.2.jzqsr=gz%2Elianjia%2Ecom|jzqct=/ershoufang/.jzqsr=sz%2Elianjia%2Ecom|jzqct=/; select_city=440300; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1657598070,1657645626,1657684359,1658070842; _qzjc=1; _jzqa=1.2045555367214675000.1656860786.1657684360.1658070843.10; _jzqc=1; _jzqckmp=1; _gid=GA1.2.702690955.1658070845; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1658073765; _qzja=1.938727382.1656868561950.1657684360095.1658070842853.1658073754169.1658073765275.0.0.0.76.8; _qzjto=2.0.0; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOGZlNjE4ZGI1M2UyMWU3NjU4YWUzMWQxMGMwZjZmM2EwYWM3OWNlYzNjZDNhYmFiNjEyYmE3YWY1OWY0Y2Y2ZGIxM2QyYzRmMmVhMGEyYWViYmQ0MGNiNzU1ZmIxYTE5YTU4NjVmNDA3YzlkYTJjN2U3ZDk1NWE2NzQ4NzEwYTBjZjAyMGRjYzU4Mzk1OTgxZTUyZTRiNGNlYzA4ZTFjN2VkOTkyZDNkNDg0N2EyZGI4OWUyMzlmMjcyYjAxNTY4Njk2Y2E1Y2M1Y2I4M2ViMWRkYjZlNDkxMjg5MDNhZmI2Zjc4ZjQ5NDBmNWUyN2JjZWJjYjA1NjI1MWU1OTBjZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIwYjQyZTc0Y1wifSIsInIiOiJodHRwczovL3N6LmxpYW5qaWEuY29tLy94aWFvcXUvZGl3YW5nLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
}

# 链家城市子域名 URL 字典
with open(Path(BASE_DIR).joinpath("subdomain.json"), "r") as f:
    _subdomain = f.read()

SUB_DOMAIN_DICT = json.loads(_subdomain)

# 最大可开启的异步线程数量
MAX_SEMAPHORE = 100

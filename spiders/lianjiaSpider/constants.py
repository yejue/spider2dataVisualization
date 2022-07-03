import json
from pathlib import Path

# 当前文件位置
BASE_DIR = Path(__file__).resolve().parent

# 链家 HEADERS
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
}

# 链家城市子域名 URL 字典
with open(Path(BASE_DIR).joinpath("subdomain.json"), "r") as f:
    _subdomain = f.read()

SUB_DOMAIN_DICT = json.loads(_subdomain)

# 最大可开启的异步线程数量
MAX_SEMAPHORE = 100

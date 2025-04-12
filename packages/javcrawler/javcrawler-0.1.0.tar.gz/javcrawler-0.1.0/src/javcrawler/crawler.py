import time
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup

from .config import config
from .logger import logger


class ProxyBlockedException(Exception):
    pass


class SearchResult:
    def __init__(self, url: str, num: str, title: str):
        self.url = url
        self.num = num
        self.title = title

    def __str__(self):
        return f"{self.url}  {self.num}  {self.title}"


class Magnet:
    def __init__(self, magnet: str, size: str, tags: list):
        self.magnet = magnet
        self.size = size
        self.tags = tags  # 高清/字幕/流出/破解/无码
        self.score = 5 * ("流出" in tags) + 4 * ("高清" in tags) + 3 * ("字幕" in tags)

    def __str__(self):
        return f"{self.magnet}  {self.size} {'|'.join(self.tags)}"

    def __lt__(self, other):
        return self.score < other.score


class Crawler:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = config.url
        self.max_entries = config.entries
        self.session.headers.update(
            {
                "User-Agent": config.ua,
            }
        )
        self.proxies = {
            "http": config.http_proxy,
            "https": config.https_proxy,
        }

    def _get_html(self, url, params=None, timeout=5, retry=3) -> str:
        failed = 0
        for _ in range(retry):
            try:
                logger.info(f"正在请求 url: {url}")
                r = self.session.get(
                    url,
                    params=params,
                    timeout=timeout,
                    proxies=self.proxies,
                    cookies={"over18": "1"},
                ).text
                logger.debug(len(r))
                if len(r) < 1000:
                    logger.debug(r)
                    logger.error("返回内容极短, 疑似代理被禁用, 请检查")
                    time.sleep(5)
                    continue
                return r
            except requests.exceptions.Timeout:
                logger.error(f"请求 url ({url}) 超时")
                failed += 1
            except requests.exceptions.ProxyError:
                logger.error("网络代理错误")
                failed += 1
            except requests.exceptions.RequestException as e:
                if e.response is not None:
                    logger.error(f"请求 url ({url}) 返回了错误的状态码：{e.response.status_code}")
                else:
                    logger.error(f"请求 url ({url}) 时发生错误：{e}")
                failed += 1
            except:
                logger.error("未知错误")
                raise
            finally:
                if failed >= retry:
                    logger.error(f"Failed {retry} times on {url} ")
                    raise

    def search_by_keyword(self, keyword: str) -> List[SearchResult]:
        """
        在 javdb 上搜索指定关键词, 返回所有搜索结果的 url、番号及标题, 若某个结果的番号与关键词完全一致则仅返回该条
        """
        params = {"q": keyword, "f": "download"}  # f=download 筛选有磁链的结果
        html_code = self._get_html(self.base_url + "/search", params=params)
        soup = BeautifulSoup(html_code, "lxml")
        res_list = []
        x = soup.find_all("div", class_="item")  # xpath: //div[@class="item"] 搜索结果
        if x:
            for res in x:  # res: bs4.element.Tag
                try:
                    true_url: str = res.a["href"]  # 详情页 url. e.g. /v/JAy0B 则完整 url 为 https://javdb.com/v/JAy0B
                    title: str = res.a["title"]  # 影片标题, javdb 的标题比较混乱, 有的以番号开头, 有的不包含番号
                    av_num: str = res.find(
                        "div", class_="video-title"
                    ).strong.string.strip()  # 可能为番号的文本, 欧美影片为系列名
                    if av_num == keyword:
                        return [SearchResult(true_url, av_num, title)]
                except KeyError or AttributeError:
                    logger.error("解析 html 元素失败")
                    logger.debug(f"原始网页: {res.prettify()}")
                    continue
                except:
                    logger.error("未知错误")
                    logger.debug(f"原始网页: {res.prettify()}")
                    raise
                res_list.append(SearchResult(true_url, av_num, title))
            return res_list
        else:
            Path("failed").mkdir(exist_ok=True)
            Path(f"failed/{keyword}.html").write_text(html_code, encoding="utf-8")
            logger.info(f"无法定位元素, 解析器可能失效, 已保存网页到 failed/{keyword}.html")
            return []

    def get_magnets(self, ture_url: str) -> List[Magnet]:
        """
        根据影片详情页 url e.g. /v/JAy0B 获取该影片的所有磁链及其信息(大小/文件数/清晰度/是否有字幕)
        """
        magnets = []
        full_url = self.base_url + ture_url
        html_code = self._get_html(full_url)
        soup = BeautifulSoup(html_code, "lxml")
        x = soup.find_all("div", class_="magnet-name")  # //div[@class="magnet-name"] 磁链列表
        if not x:
            return []
        for res in x[: self.max_entries]:
            magnet = res.a["href"]  # 磁链 a/@href
            size = res.a.find("span", class_="meta").string.strip()  # 文件大小及个数 a/span[@class="meta"]
            name = res.a.find("span", class_="name").string.strip()  # 磁链标题 a/span[@class="name"]
            tags = []
            if "破解" in name:
                tags.append("破解")
            if "流出" in name:
                tags.append("流出")
            if "uncensored" in name:
                tags.append("无码")
            if s := res.a.find("div", class_="tags"):
                tags.extend([x.string.strip() for x in s.find_all("span")])  # 磁链 tag, 高清/字幕 a/div/span
            magnets.append(Magnet(magnet, size, tags))
        return magnets

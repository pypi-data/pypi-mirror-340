import argparse
import time
from typing import Optional

from .config import config
from .crawler import Crawler, Magnet
from .logger import log_to_console, logger
from .utils import _get_input_until_success, _handle_num, _islegal_path, _list2str


class Program:
    def __init__(self):
        self.interval = config.interval
        self.failed = []
        self.crawler = Crawler()
        self.auto = True

    def _search_once(self, keyword):
        print(f"正在搜索 {keyword} ...")
        s = self.crawler.search_by_keyword(keyword)
        if len(s) == 0:
            print(f"未搜索到 {keyword} 相关影片")
        elif len(s) == 1:
            magnets = self.crawler.get_magnets(s[0].url)
            if self.auto:
                print(max(magnets))
                return
            print(_list2str(magnets))
        else:
            res_list = [f"{x.num}   {x.title}" for x in s]
            print(_list2str(res_list))
            select = _get_input_until_success("请选择搜索结果: ")
            magnets = self.crawler.get_magnets(s[select - 1].url)
            if self.auto:
                print(max(magnets))
                return
            print(_list2str(magnets))
        input("Press any key to continue...")

    def _batch_search_once(self, keyword) -> Optional[Magnet]:
        print(f"正在搜索 {keyword} ...")
        s = self.crawler.search_by_keyword(keyword)
        if len(s) == 0:
            print(f"未搜索到 {keyword} 相关影片")
        elif len(s) == 1:
            magnets = self.crawler.get_magnets(s[0].url)
            if self.auto:
                r = max(magnets)
                print(f"选中结果: {r}")
                return r
            print(_list2str(magnets))
            select = _get_input_until_success("请选择磁链:")
            return magnets[select - 1]
        else:
            if self.auto:
                print("自动模式下跳过未完全匹配的关键词")
                self.failed.append(keyword)
                return None
            res_list = [f"{x.num}   {x.title}" for x in s]
            print(_list2str(res_list))
            select = _get_input_until_success("请选择搜索结果: ")
            magnets = self.crawler.get_magnets(s[select - 1].url)
            print(_list2str(magnets))
            select = _get_input_until_success("请选择磁链:")
            return magnets[select - 1]

    def run(self):
        print("========================================")
        print("          JavDB Magnet Crawler          ")
        while True:
            print("========================================")
            s = input(
                f"1. 直接输入关键词或番号进行搜索\n"
                f"2. 输入 f 进行读取文件搜索\n"
                f"3. 输入 a 切换自动/手动模式 (当前: {'自动' if self.auto else '手动'}模式)\n"
                f"4. 输入 q 退出程序\n"
                f"请输入:"
            )
            if s == "q":
                exit(0)
            elif s == "a":
                self.auto = not self.auto
                print(f"已切换至{'自动' if self.auto else '手动'}模式.")
                if self.auto:
                    print(
                        "自动模式下, 将直接选择最接近的搜索结果, 然后按 高清字幕 -> 高清 -> 字幕 -> 第一个 优先级选择最优磁链. "
                        "在该模式下, 读取文件搜索将跳过未完全匹配的关键词, 并将其记录在 failed.txt 中."
                    )
                else:
                    print("手动模式下, 当存在多个搜索结果时, 将由用户从中选择.")
            elif s == "f":
                file_path = _get_input_until_success("请输入文件路径(默认为 list.txt): ", _islegal_path)
                with open(file_path, "r", encoding="utf-8") as f:
                    if file_path.endswith(".txt"):
                        keywords = f.readlines()
                        keywords = [t for x in keywords if (t := x.strip())]
                    elif file_path.endswith(".json"):
                        import json

                        d = json.load(f)
                        keywords = [item["number"] for item in d]
                        if not keywords:
                            print("无法解析 json, number 字段不存在")
                            continue
                with open("magnets.txt", "w+", encoding="utf-8") as f:
                    start_time = time.time()
                    for keyword in keywords:
                        keyword = _handle_num(keyword)
                        r = self._batch_search_once(keyword)
                        if r:
                            f.write(r.magnet + "\n")
                        time.sleep(self.interval)
                    end_time = time.time()
                    logger.info(f"处理了 {len(keywords)} 个关键词, 共耗时 {end_time - start_time:.2f} 秒")
                if len(self.failed) > 0:
                    with open("failed.txt", "w") as f:
                        f.writelines("\n".join(self.failed))
                    print("以下关键词未完全匹配, 已记录在 failed.txt 中:")
                    print(_list2str(self.failed))
            else:
                self._search_once(_handle_num(s))


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug mode", default=False)
    args = parser.parse_args()
    if args.debug:
        log_to_console("DEBUG")
    else:
        log_to_console("INFO")
    Program().run()

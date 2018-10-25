# -*- coding: utf-8 -*-

from db.redis_client import redis_cli
from util.decorator import timethis
from util.common import logger
from bs4 import BeautifulSoup
import requests
import time


class BaiduHotGenerator:
    '''百度热点内容获取'''

    @timethis
    def crawl_hot_words(self, sleep_time):
        # 实时热点 今日热点 七日热点 民生热点 娱乐热点 体育热点
        hot_topic_urls = ('http://top.baidu.com/buzz?b=1&c=513&fr=topcategory_c513',
                          'http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1_c513',
                          'http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b1_c513',
                          'http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513',
                          'http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513',
                          'http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513')
        for url in hot_topic_urls:
            try:
                req = requests.get(url=url)
                req.encoding = req.apparent_encoding
                bf = BeautifulSoup(req.text, "html.parser")
                for tp in map(lambda x: x.string, bf.find_all('a', class_="list-title")):
                    redis_cli.save_keyword(tp)
                    time.sleep(sleep_time)
            except Exception as e:
                logger.error(e)

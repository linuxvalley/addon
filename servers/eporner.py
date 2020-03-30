# -*- coding: utf-8 -*-
import re

from core import httptools
from platformcode import config
from platformcode import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    global data
    data = httptools.downloadpage(page_url).data
    if "<h2>WE ARE SORRY</h2>" in data or '<title>404 Not Found</title>' in data:
        return False,  config.get_localized_string(70449) % "eporner"
    return True, ""


def get_video_url(page_url, video_password):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []
    data = httptools.downloadpage(page_url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>|<br/>", "", data)
    patron = "EP: {vid: '([^']+)',hash: '([^']+)'"
    vid, hash = re.compile(patron, re.DOTALL).findall(data)[0]
    hash = int_to_base36(int(hash[0:8], 16)) + int_to_base36(int(hash[8:16], 16)) + int_to_base36(
        int(hash[16:24], 16)) + int_to_base36(int(hash[24:32], 16))
    url = "https://www.eporner.com/xhr/video/%s?hash=%s" % (vid, hash)
    jsondata = httptools.downloadpage(url).json
    for source in jsondata["sources"]["mp4"]:
        url = jsondata["sources"]["mp4"][source]["src"]
        title = source.split(" ")[0]
        video_urls.append(["[eporner] %s"% title, url])
    return video_urls
    # return sorted(video_urls, key=lambda i: int(i[0].split("p")[1]))




def int_to_base36(num):
    """Converts a positive integer into a base36 string."""
    assert num >= 0
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()

    res = ''
    while not res or num > 0:
        num, i = divmod(num, 36)
        res = digits[i] + res
    return res


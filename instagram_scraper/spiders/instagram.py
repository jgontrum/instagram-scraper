# -*- coding: utf-8 -*-
import json
import re
import urllib.parse

from scrapy.spiders import CrawlSpider

from instagram_scraper.items import InstagramScraperItem


class InstagramSpider(CrawlSpider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    def __init__(self, hashtag=None, *a, **kwargs):
        super().__init__(*a, **kwargs)
        if not hashtag:
            hashtag = "followme"

        self.start_urls = [self.generate_url(hashtag)]

    def generate_url(self, hashtag, cursor=None, limit=100):
        hash = "298b92c8d7cad703f7565aa892ede943"

        vars = {
            "tag_name": hashtag,
            "first": limit
        }

        if cursor:
            vars["after"] = cursor

        vars = urllib.parse.quote_plus(json.dumps(vars))

        return f"https://www.instagram.com/graphql/query/" \
               f"?query_hash={hash}&variables={vars}"

    def extract_hashtags(self, text):
        return [t.lower().strip() for t in re.findall(r"#(\w+)", text)]

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())
        page_info = resp["data"]["hashtag"]["edge_hashtag_to_media"][
            "page_info"]

        cursor = page_info["end_cursor"] if page_info["has_next_page"] else None
        current_hashtag = resp["data"]["hashtag"]["name"].lower()
        hashtags = set()

        self.logger.info(f"Current Hashtag: #{current_hashtag}")

        for node in resp["data"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
            node = node["node"]

            try:
                item = {
                    "id": node["shortcode"],
                    "timestamp": node["taken_at_timestamp"],
                    "user": node["owner"]["id"],
                    "likes": node["edge_liked_by"]["count"],
                    "comments": node["edge_media_to_comment"]["count"],
                    "text":
                        node["edge_media_to_caption"]["edges"][0]["node"][
                            "text"],
                    "photo_low": list(filter(
                        lambda t: t["config_width"] == 150,
                        node["thumbnail_resources"]
                    ))[0]["src"]
                }

                item_hashtags = self.extract_hashtags(item["text"])

                if not item_hashtags:
                    continue

                item["hashtags"] = " ".join(item_hashtags)
                hashtags = hashtags.union(set(item_hashtags))

                yield InstagramScraperItem(item)
            except IndexError or TypeError:
                continue

        for hashtag in hashtags:
            url = self.generate_url(hashtag)
            yield response.follow(url, priority=-10)

        if cursor:
            url = self.generate_url(current_hashtag, cursor=cursor)
            yield response.follow(url, priority=-100)

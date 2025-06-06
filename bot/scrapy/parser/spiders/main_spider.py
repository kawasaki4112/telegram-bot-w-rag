import json
import os
import asyncio
import re
from asyncio import WindowsSelectorEventLoopPolicy
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from bot.llm.llm import create_embeddings

class MainSpider(CrawlSpider):
    url = os.getenv('URL', 's-vfu.ru')
    name = 'main_spider'
    start_urls = [f'https://{url}/']
    allowed_domains = [url, f'www.{url}']
    output_file = 'bot/scrapy/parsed_data/output.json'

    rules = (
        Rule(LinkExtractor(allow=r's-vfu\.ru'), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.existing_urls = set()
        self.items = []
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    self.existing_urls = {item['url'] for item in data}
                    self.items.extend(data)
                except json.JSONDecodeError:
                    pass

    def parse_item(self, response):
        if response.url in self.existing_urls:
            return

        raw_texts = response.xpath(
            "//div[@id='content']//text()"
            "[not(ancestor::script) and not(ancestor::style)]"
        ).getall()

        texts = []
        for t in raw_texts:
            t = t.strip()
            if not t:
                continue
            if re.search(r"[{};=<>/\\\(\)]", t):
                continue
            texts.append(t)

        if texts:
            item = {
                'url': response.url,
                'data': ' '.join(texts)
            }
            self.existing_urls.add(response.url)
            self.items.append(item)
            yield item

    def closed(self, reason):
        if self.items:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.items, f, ensure_ascii=False, indent=4)
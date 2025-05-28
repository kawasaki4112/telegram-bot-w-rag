import json
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sqlalchemy.ext.asyncio import AsyncSession

from bot.llm.llm import create_embeddings

class MainSpider(CrawlSpider):
    url = os.getenv('URL', 's-vfu.ru')
    name = 'main_spider'
    allowed_domains = [url]
    start_urls = [f'http://{url}/']
    output_file = 'bot/scrapy/parsed_data/output.json'

    rules = (
        Rule(LinkExtractor(allow=r's-vfu\.ru'), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.existing_urls = set()
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    self.existing_urls = {item['url'] for item in data}
                except json.JSONDecodeError:
                    pass

    def parse_item(self, response):
        if response.url in self.existing_urls:
            return

        content_div = response.css('div#content')
        if content_div:
            data = []
            p_content = content_div.css('p')
            if p_content:
                for element in content_div.css('h1, h2, h3, h4, h5, h6, p, br, div'):
                    text = element.css('::text').get()
                    if text and text.strip():
                        data.append(text.strip())
            
            if data:
                result = {
                    'url': response.url,
                    'data': ' '.join(data)
                }
                self.existing_urls.add(response.url)
                yield result

    def closed(self, reason):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            data = [{'url': url, 'data': item['data']} for url, item in zip(self.existing_urls, self.crawler.stats.get_value('item_scraped_count'))]
            json.dump(data, f, ensure_ascii=False, indent=4)
            create_embeddings(data)
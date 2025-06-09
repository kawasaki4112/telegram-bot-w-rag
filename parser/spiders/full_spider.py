import os
from urllib.parse import urlparse
from datetime import datetime, timedelta

import scrapy
from scrapy.http import Request
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('SITE_URL')
STALE_DAYS = int(os.getenv('STALE_DAYS', 90))

class FullSpider(scrapy.Spider):
    name = 'full_spider'
    allowed_domains = [urlparse(BASE_URL).netloc]
    start_urls = [BASE_URL]

    def parse(self, response):
        self.logger.info(f"Parsing page: {response.url}")
        for href in response.css('a::attr(href)').getall():
            full_url = response.urljoin(href)
            if urlparse(full_url).netloc != self.allowed_domains[0]:
                continue
            yield Request(full_url, method='HEAD', callback=self.check_freshness, meta={'original_url': full_url})

    def check_freshness(self, response):
        url = response.meta['original_url']
        last_mod_header = response.headers.get('Last-Modified')
        if last_mod_header:
            try:
                last_mod = datetime.strptime(last_mod_header.decode(), '%a, %d %b %Y %H:%M:%S %Z')
                if last_mod < datetime.utcnow() - timedelta(days=STALE_DAYS):
                    self.logger.info(f"Skipping stale URL: {url}")
                    return
            except Exception:
                self.logger.warning(f"Не удалось распарсить Last-Modified для {url}, продолжаем")
        yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        title = response.css('title::text').get(default='').strip()
        paragraphs = response.css('p::text').getall()
        body = '\n'.join([p.strip() for p in paragraphs if p.strip()])
        yield {
            'url': response.url,
            'data': f"{title}\n{body}",
        }
        for href in response.css('a::attr(href)').getall():
            next_url = response.urljoin(href)
            if urlparse(next_url).netloc == self.allowed_domains[0]:
                yield Request(next_url, method='HEAD', callback=self.check_freshness, meta={'original_url': next_url})
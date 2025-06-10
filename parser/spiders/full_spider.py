import os
import re
from datetime import datetime
from urllib.parse import urlparse
from io import BytesIO

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from dotenv import load_dotenv

from pdfminer.high_level import extract_text
import pdfplumber

load_dotenv(override=True)
BASE_URL = os.getenv('SITE_URL')

domain = urlparse(BASE_URL).netloc
www_domain = 'www.' + domain if not domain.startswith('www.') else domain

class FullSpider(CrawlSpider):
    name = 'full_spider'

    allowed_domains = [domain, www_domain]
    start_urls = [BASE_URL]

    is_check_date = os.getenv('IS_CHECK_DATE', 'False').lower() in ('true')
    year = datetime.now().year
    prev_year = year - 1
    four_digits_re = re.compile(r'(\d{4})')

    rules = (
        Rule(
            LinkExtractor(allow_domains=allowed_domains),
            callback='parse_item',
            follow=True,
            process_links='filter_links'
        ),
    )

    def filter_links(self, links):
        if not self.is_check_date:
            return links

        filtered = []
        for link in links:
            if self.is_valid_year_in_url(link.url):
                filtered.append(link)
            else:
                self.logger.debug(f"Skipping URL (invalid year): {link.url}")
        return filtered

    def is_valid_year_in_url(self, url: str) -> bool:
        for match in self.four_digits_re.findall(url):
            y = int(match)
            if y not in (self.year, self.prev_year):
                return False
        return True

    def parse_item(self, response):
        content_type = response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore')

        if 'application/pdf' in content_type:
            self.logger.info(f"Processing PDF: {response.url}")

            fp = BytesIO(response.body)
            with pdfplumber.open(fp) as pdf:
                num_pages = len(pdf.pages)
                has_table = any(page.extract_tables() for page in pdf.pages)

            if not has_table and num_pages > 5:
                self.logger.info(
                    f"Skip PDF (tables: {has_table}, pages: {num_pages}): {response.url}"
                )
                return

            text = self.parse_pdf(response.body)
            yield {
                'url': response.url,
                'text': text
            }
            return

        if 'text/html' not in content_type:
            return

        self.logger.info(f"Parsing HTML page: {response.url}")
        title = response.css('title::text').get(default='').strip()
        paragraphs = response.css('p::text').getall()
        body = ' '.join(p.strip() for p in paragraphs if p.strip())
        yield {'url': response.url, 'text': f"{title} {body}"}

    def parse_pdf(self, data: bytes) -> str:
        fp = BytesIO(data)
        text = extract_text(fp)
        return text


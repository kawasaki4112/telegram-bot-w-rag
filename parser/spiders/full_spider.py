import os
import re
from datetime import datetime
from urllib.parse import urlparse
from io import BytesIO

import scrapy
from dotenv import load_dotenv

from pdfminer.high_level import extract_text
import pdfplumber


load_dotenv(override=True)
BASE_URL = os.getenv('SITE_URL')

class FullSpider(scrapy.Spider):
    name = 'full_spider'

    domain = urlparse(BASE_URL).netloc
    www_domain = 'www.' + domain if not domain.startswith('www.') else domain
    allowed_domains = [domain, www_domain]
    start_urls = [BASE_URL]

    is_check_date = os.getenv('IS_CHECK_DATE', 'False').lower() in ('true')
    year = datetime.now().year
    prev_year = year - 1
    four_digits_re = re.compile(r'(\d{4})')

    def is_valid_year_in_url(self, url: str) -> bool:
        for match in self.four_digits_re.findall(url):
            y = int(match)
            if y not in (self.year, self.prev_year):
                return False
        return True

    def parse(self, response):
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

        # — ветка для HTML остаётся без изменений —
        if 'text/html' not in content_type:
            return

        self.logger.info(f"Parsing HTML page: {response.url}")
        title = response.css('title::text').get(default='').strip()
        paragraphs = response.css('p::text').getall()
        body = ' '.join(p.strip() for p in paragraphs if p.strip())
        yield {'url': response.url, 'text': f"{title} {body}"}

        for href in response.css('a::attr(href)').getall():
            full_url = response.urljoin(href)
            netloc = urlparse(full_url).netloc

            if netloc not in self.allowed_domains:
                continue
            if self.is_check_date and not self.is_valid_year_in_url(full_url):
                self.logger.debug(f"Skipping URL (invalid year): {full_url}")
                continue
            yield scrapy.Request(full_url, callback=self.parse)

    def parse_pdf(self, data: bytes) -> str:
        fp = BytesIO(data)
        text = extract_text(fp)
        return text
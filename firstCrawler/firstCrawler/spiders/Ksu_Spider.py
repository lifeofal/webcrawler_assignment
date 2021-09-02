import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import hashlib


# create a way to scrape webpages, store and catigoirze which pages have email addresses in raw format.

# link extractor can only use links with 'kennesaw.edu' in the domain
# no dupe links
class ksuSpider(scrapy.Spider):
    name = "KSUSpider"
    allowed_domains = ["kennesaw.edu"]

    rules = (
        Rule(LinkExtractor(allow=('.edu')), callback='parse', follow=True)
    )

    start_urls = [
        'https://www.kennesaw.edu'
    ]

    def parse(self, response):

        url = response.request.url
        page = response.body
        title = response.css('title::text').get()
        pageid = hashlib.md5(url.encode())

        entry = dict.fromkeys(['pageid', 'url', 'title', 'body', 'emails'])

        entry['title'] = title
        entry['url'] = url
        entry['pageid'] = pageid.hexdigest()[:5]
        entry['emails'] = response.css('a[href ^= \"mailto\"]::text').getall(),
        soup = BeautifulSoup(page, 'html.parser')
        body = soup.get_text(separator=' ', strip='true')
        entry['body'] = body

        filename = f'{title}.html'
        with open(filename, 'w') as f:
            f.write(body)

        for info in response.css('div.site_wrapper'):
            entry['emails'] = info.css('a[href ^= \"mailto\"]::text').getall(),
            yield entry

        next_page = response.css('div#gold_bar a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

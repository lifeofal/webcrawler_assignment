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
        'https://www.kennesaw.edu',
        'https://ccse.kennesaw.edu/fye/staff.php',
    ]


    def parse(self, response):

        url = response.request.url

        page = response.body
        title = response.css('title::text').get()
        pageId = hashlib.md5(url.encode())

        entry = dict.fromkeys(['pageid', 'url', 'title', 'body', 'emails'])

        entry['title'] = title
        entry['url'] = url
        entry['pageid'] = pageId.hexdigest()[:5]
        #entry['emails'] = response.css('a[href ^= \"mailto\"]::text').getall(),
        soup = BeautifulSoup(page, 'html.parser')
        body = soup.get_text(separator=' ', strip='true')
        entry['body'] = body




        # filename = f'{title}.html'
        # with open(filename, 'w') as f:
        #     f.write(body)

        for info in response.css('div.site_wrapper'):
            entry['emails'] = info.css('a[href ^= \"mailto\"]::text').getall()
        yield entry



        # links = response.css('div.site_wrapper a[href ^= \"https\"]::attr(href)').extract()
        # for link in links:
        #     if link is not None:
        #         link = response.urljoin(link)
        #         yield scrapy.Request(link, callback=self.parse)

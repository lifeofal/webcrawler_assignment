import scrapy

class KsuSpider(scrapy.Spider):
    name = "KSUSpider"

    def start_requests(self):
        urls = [
            'http://www.kennesaw.edu',
            'http://ccse.kennesaw.edu',
            'https://ccse.kennesaw.edu/fye/index.php',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        #create a way to scrape webpages, store and catigoirze which pages have email addresses in raw format.

        #link extractor can only use links with 'kennesaw.edu' in the domain
        #no dupe links

        for email in response.xpath('//a[contains(@href,\'@\')'):
            yield{
                #'email': email.xpath('//*[contains(text(), \'@\')]').get()
                'Email': email.xpath('//a[starts-with(@href, \'mailto\')]/text()').get()
                #
            }




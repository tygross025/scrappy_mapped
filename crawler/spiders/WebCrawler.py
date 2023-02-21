from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from crawler.items import Website


class WebCrawler(CrawlSpider):
    name = 'web_crawler'
    start_urls = None

    rules = (
        Rule(LinkExtractor(), callback='parse_item'),
    )

    def parse_item(self, response):
        """Extract the current url as well as all link urls from page"""

        site = Website()
        # Populate domain field with url (will be processed into domain in GetDomainPipeline)
        site['domain'] = response.url
        linked_to = []
        for link in self.rules[0].link_extractor.extract_links(response):
            linked_to.append(link.url)
            yield Request(link.url, callback=self.parse_item)

        site['linked_to'] = linked_to
        yield site

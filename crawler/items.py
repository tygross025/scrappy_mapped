import scrapy


class Website(scrapy.Item):
    domain = scrapy.Field()
    address = scrapy.Field()
    linked_to = scrapy.Field()


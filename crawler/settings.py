# Scrapy settings for crawler project

LOG_LEVEL = 'INFO'

BOT_NAME = "web_crawler"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

DEPTH_LIMIT = 1

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "crawler.pipelines.GetDomainPipeline": 500,
    "crawler.pipelines.ExportItemsPipeline": 900,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

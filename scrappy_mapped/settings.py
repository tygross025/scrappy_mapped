# Scrapy settings for scrappy_mapped project

LOG_LEVEL = 'INFO'

BOT_NAME = "scrappy_mapped"

SPIDER_MODULES = ["scrappy_mapped.spiders"]
NEWSPIDER_MODULE = "scrappy_mapped.spiders"

DEPTH_LIMIT = 1

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "scrappy_mapped.pipelines.GetDomainPipeline": 500,
    "scrappy_mapped.pipelines.ExportItemsPipeline": 900,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

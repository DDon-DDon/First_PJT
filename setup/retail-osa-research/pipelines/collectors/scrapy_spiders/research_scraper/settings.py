# Scrapy settings for research_scraper project

BOT_NAME = "research_scraper"

SPIDER_MODULES = ["research_scraper.spiders"]
NEWSPIDER_MODULE = "research_scraper.spiders"

# Crawl responsibly
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 8

# Feed exports
FEEDS = {
    "../../data/raw/crawl/%(name)s.jsonl": {
        "format": "jsonlines",
        "encoding": "utf8",
        "overwrite": False,
    }
}

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "../../logs/scrapy.log"

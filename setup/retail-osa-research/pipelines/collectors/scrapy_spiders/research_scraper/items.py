import scrapy


class DocItem(scrapy.Item):
    """크롤링된 문서 아이템"""
    doc_id = scrapy.Field()
    source_id = scrapy.Field()
    url = scrapy.Field()
    retrieved_at = scrapy.Field()
    title = scrapy.Field()
    published_at = scrapy.Field()
    author = scrapy.Field()
    language = scrapy.Field()
    content_text = scrapy.Field()
    keyword_refs = scrapy.Field()
    tags = scrapy.Field()

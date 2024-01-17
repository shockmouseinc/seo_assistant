import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from scrapy.http import Response
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from seo_crawler.seo_crawler.items import CrawledContentItem
from typing import Iterable, Any
from scrapy import Request


class SerpSpider(scrapy.Spider):
    name = 'serp_spider'

    custom_settings = {

    }

    def __init__(self, urls=None, *args, **kwargs):
        super(SerpSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls or [] # Accept URLs passed from the calling service

    def parse(self, response: Response, **kwargs: Any) -> Any:
        # Example of using Item and ItemLoader to extract and process the content:
        loader = ItemLoader(item=CrawledContentItem(), response=response)
        loader.default_output_processor = TakeFirst()

        # Use custom xpaths to extract the data
        loader.add_xpath('text', '//body//text()')
        # ... add more fields here as needed

        yield loader.load_item()

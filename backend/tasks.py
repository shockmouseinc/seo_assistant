from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from seo_crawler.seo_crawler.spiders.serp_spider import SerpSpider

@shared_task
def run_serp_spider(urls):
    process = CrawlerProcess(get_project_settings())
    process.crawl(SerpSpider, urls=urls)
    process.start()
    pass

@shared_task
def simple_test_task():
    print("The task ran!")
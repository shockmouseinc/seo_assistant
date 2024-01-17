from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from seo_crawler.seo_crawler.spiders.serp_spider import SerpSpider
import os
from serpapi import GoogleSearch

def get_search_results(keyword):
    # SERP API key is defined in env variables
    serpapi_key = os.environ.get('SERPAPI_API_KEY')

    if not serpapi_key:
        raise ValueError("The SERPAPI_API_KEY environment variable is not set.")

    params = {
        "q": keyword,
        "location": "New York, New York",
        "hl": "en",
        "gl": "us",
        "api_key": serpapi_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Process and extract top 5 organic search results
    top_results = results.get("organic_results", [])[:5]
    search_results_info = [{
        "position": result.get("position"),
        "title": result.get("title"),
        "link": result.get("link"),
        "snippet": result.get("snippet"),
        "displayed_link": result.get("displayed_link"),
        # Add additional fields if needed...
    } for result in top_results]

    return search_results_info

def run_serp_spider(urls):
    # Start the Scrapy crawler
    process = CrawlerProcess(get_project_settings())
    process.crawl(SerpSpider, urls = urls)
    process.start()
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.scraper.spiders.dopagent_spider import DopagentSpider

process = CrawlerProcess()
process.crawl(DopagentSpider)
process.start()

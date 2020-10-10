from scrapy.crawler import CrawlerProcess
from scraper.scraper.spiders import DopagentSpider

def main():
    process = CrawlerProcess()
    process.crawl(DopagentSpider)
    process.start()

if __name__ == "__main__":
    main()

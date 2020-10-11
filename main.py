from scrapy.crawler import CrawlerProcess

from scraper.scraper.spiders import AccountsSpider


def main(agent_id, password):
    process = CrawlerProcess()
    process.crawl(AccountsSpider, agent_id, password)
    process.start()


if __name__ == "__main__":
    agent_id = ''
    password = ''
    main(agent_id, password)

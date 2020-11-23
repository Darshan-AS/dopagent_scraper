import json
from scraper.items import AccountItem

from itemadapter import ItemAdapter


class AccountPipeline:
    def open_spider(self, spider):
        file_name = spider.agent_id if hasattr(spider, 'agent_id') else 'common'
        self.file = open(f'./accounts/{file_name}.json', 'a')

    def process_item(self, item, spider):
        if not isinstance(item, AccountItem):
            return

        item_str = json.dumps(ItemAdapter(item).asdict(), indent=4, default=str) + "\n"
        self.file.write(item_str)
        return item

    def close_spider(self, spider):
        self.file.close()

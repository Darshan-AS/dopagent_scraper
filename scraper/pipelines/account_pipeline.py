import json
from pathlib import Path

from itemadapter import ItemAdapter

from scraper.items import AccountItem


# pylint: disable=attribute-defined-outside-init
class AccountPipeline:
    ACCOUNTS_DIR = 'accounts'

    def open_spider(self, spider):
        file_name = spider.agent_id if hasattr(spider, 'agent_id') else 'common'
        path_to_file = Path.cwd() / self.ACCOUNTS_DIR
        path_to_file.mkdir(exist_ok=True)
        self.file = open(path_to_file / f'{file_name}.json', 'a')

    def process_item(self, item, _):
        if not isinstance(item, AccountItem):
            return

        item_str = json.dumps(ItemAdapter(item).asdict(), indent=4, default=str) + "\n"
        self.file.write(item_str)
        return item

    def close_spider(self, _):
        self.file.close()

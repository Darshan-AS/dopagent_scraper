import json
from itemadapter import ItemAdapter


class AccountPipeline:

    def open_spider(self, spider):
        self.file = open('items.json', 'a')


    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

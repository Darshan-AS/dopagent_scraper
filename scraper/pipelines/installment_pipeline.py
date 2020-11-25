import json

from itemadapter import ItemAdapter


class InstallmentPipeline:
    def open_spider(self, spider):
        file_name = (
            spider.reference_number if hasattr(spider, 'reference_number') else 'common'
        )
        self.file = open(f'./reports/{file_name}.json', 'w')

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

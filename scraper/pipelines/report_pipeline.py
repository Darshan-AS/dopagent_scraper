import json
from base64 import b64decode
from pathlib import Path

from itemadapter import ItemAdapter

from scraper.items import ReportItem


# pylint: disable=attribute-defined-outside-init
class ReportPipeline:
    REPORTS_DIR = 'reports'

    def open_spider(self, spider):
        file_name = (
            spider.reference_number if hasattr(spider, 'reference_number') else 'common'
        )
        extension = (
            spider.report_type.name.lower() if hasattr(spider, 'report_type') else ''
        )

        path_to_file = Path.cwd() / self.REPORTS_DIR
        path_to_file.mkdir(exist_ok=True)
        self.transactions_file = open(path_to_file / f'{file_name}.json', 'w')
        self.raw_file = open(path_to_file / f'{file_name}.{extension}', 'wb')

    def process_item(self, item, _):
        if not isinstance(item, ReportItem):
            return

        for transaction in item.get('transactions', []):
            transaction_str = (
                json.dumps(
                    ItemAdapter(transaction).asdict(),
                    indent=4,
                    default=str,
                )
                + "\n"
            )
            self.transactions_file.write(transaction_str)
        self.raw_file.write(b64decode(item.get('base64_bytes', '')))
        return item

    def close_spider(self, _):
        self.transactions_file.close()
        self.raw_file.close()

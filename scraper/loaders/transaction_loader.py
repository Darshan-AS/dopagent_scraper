from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class TransactionLoader(ItemLoader):

    default_output_processor = TakeFirst()

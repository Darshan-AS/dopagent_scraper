from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class InstallmentLoader(ItemLoader):

    default_output_processor = TakeFirst()

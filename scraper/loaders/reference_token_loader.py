from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class ReferenceTokenLoader(ItemLoader):

    default_output_processor = TakeFirst()

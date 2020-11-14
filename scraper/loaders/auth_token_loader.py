import scraper.constants as CONST
from itemloaders.processors import Compose, TakeFirst
from scrapy.loader import ItemLoader


def to_full_url():
    return Compose(TakeFirst(), lambda url: CONST.DOPAGENT_BASE_URL + url)


class AuthTokenLoader(ItemLoader):

    default_output_processor = to_full_url()

    referer_header_out = TakeFirst()

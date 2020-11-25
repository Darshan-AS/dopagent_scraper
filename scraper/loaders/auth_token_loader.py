import scraper.constants as CONST
from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def to_full_url(url):
    return CONST.DOPAGENT_BASE_URL + url


class AuthTokenLoader(ItemLoader):

    default_input_processor = MapCompose(to_full_url)
    referer_header_in = Identity()

    default_output_processor = TakeFirst()

from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

import scraper.constants as CONST


def to_full_url(url):
    return CONST.DOPAGENT_BASE_URL + url


class AuthTokenLoader(ItemLoader):

    default_input_processor = MapCompose(to_full_url)

    first_name_in = MapCompose(str.strip, str.title)
    last_name_in = MapCompose(str.strip, str.title)
    referer_header_in = Identity()

    default_output_processor = TakeFirst()

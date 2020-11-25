from datetime import datetime

from itemloaders.processors import Compose, MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def sanitize_floats(x):
    return x.replace(',', '')


def to_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%d-%b-%Y %I:%M:%S %p')


class TransactionLoader(ItemLoader):

    default_output_processor = TakeFirst()

    total_deposit_amount_in = MapCompose(str.split, sanitize_floats)
    no_of_installments_in = MapCompose(int)
    rebate_in = MapCompose(float)
    default_fee_in = MapCompose(float)
    last_created_date_and_time_in = MapCompose(to_datetime)

    total_deposit_amount_out = Compose(TakeFirst(), float)

from itemloaders.processors import Compose, Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def sanitize_floats():
    return MapCompose(lambda x: x.replace(',', ''))


def to_float():
    return Compose(TakeFirst(), float)


def to_int():
    return Compose(TakeFirst(), int)


class AccountLoader(ItemLoader):

    default_output_processor = TakeFirst()

    denomination_in = sanitize_floats()
    total_deposit_amount_in = sanitize_floats()

    denomination_out = to_float()
    total_deposit_amount_out = to_float()
    month_paid_upto_out = to_int()
    rebate_paid_out = to_float()
    default_fee_out = to_float()
    default_installments_out = to_int()
    pending_installments_out = to_int()

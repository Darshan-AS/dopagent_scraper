from datetime import datetime

from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def sanitize_floats(x):
    return x.replace(",", "")


def to_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%b-%Y").date()
    except ValueError:
        return None


class AccountLoader(ItemLoader):

    default_output_processor = TakeFirst()

    name_in = MapCompose(str.title)
    opening_date_in = MapCompose(to_date)
    denomination_in = MapCompose(sanitize_floats, float)
    total_deposit_amount_in = MapCompose(sanitize_floats, float)
    month_paid_upto_in = MapCompose(int)
    next_installment_due_date_in = MapCompose(to_date)
    date_of_last_deposit_in = MapCompose(to_date)
    rebate_paid_in = MapCompose(float)
    default_fee_in = MapCompose(float)
    default_installments_in = MapCompose(int)
    pending_installments_in = MapCompose(int)

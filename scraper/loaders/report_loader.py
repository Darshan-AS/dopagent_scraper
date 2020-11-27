from itemloaders.processors import Compose, Identity, TakeFirst
from scrapy.loader import ItemLoader


def to_str(report_type):
    return report_type.name

def to_utf8(base64_bytes):
    return base64_bytes.decode('utf-8')

class ReportLoader(ItemLoader):

    default_output_processor = TakeFirst()

    report_type_out = Compose(TakeFirst(), to_str)
    transactions_out = Identity()
    base64_bytes_out = Compose(TakeFirst(), to_utf8)

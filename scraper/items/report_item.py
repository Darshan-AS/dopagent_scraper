from scrapy.item import Field, Item


class ReportItem(Item):
    reference_number = Field()
    report_type = Field()
    transactions = Field()
    base64_bytes = Field()

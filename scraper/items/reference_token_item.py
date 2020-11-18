from scrapy.item import Field, Item


class ReferenceTokenItem(Item):
    reference_number = Field()

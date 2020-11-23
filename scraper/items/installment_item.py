from scrapy.item import Field, Item


class InstallmentItem(Item):
    reference_number = Field()
    account_number = Field()
    total_deposit_amount = Field()
    no_of_installments = Field()
    rebate = Field()
    default_fee = Field()
    status = Field()
    last_created_date_and_time = Field()

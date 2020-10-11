from scrapy.item import Field, Item


class AccountItem(Item):
    account_no = Field()
    name = Field()
    opening_date = Field()
    denomination = Field()
    total_deposit_amount = Field()
    month_paid_upto = Field()
    next_installment_due_date = Field()
    date_of_last_deposit = Field()
    rebate_paid = Field()
    default_fee = Field()
    default_installments = Field()
    pending_installments = Field()

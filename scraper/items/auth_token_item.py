from scrapy.item import Field, Item


class AuthTokenItem(Item):
    first_name = Field()
    last_name = Field()
    dashboard_url = Field()
    change_password_url = Field()
    accounts_url = Field()
    agent_enquire_screen_url = Field()
    reports_url = Field()
    referer_header = Field()

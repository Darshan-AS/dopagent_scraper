import scrapy
from scraper.scraper.items import AccountItem
from scraper.scraper.loaders import AccountLoader
from scrapy.loader import ItemLoader
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser


def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass


class DopagentSpider(scrapy.Spider):
    name = 'dopagent'
    start_urls = ['https://dopagent.indiapost.gov.in/corp/AuthenticationController?FORMSGROUP_ID__=AuthenticationFG&__START_TRAN_FLAG__=Y&__FG_BUTTONS__=LOAD&ACTION.LOAD=Y&AuthenticationFG.LOGIN_FLAG=3&BANK_ID=DOP&AGENT_FLAG=Y']

    custom_settings = {
        'ITEM_PIPELINES': {'scraper.scraper.pipelines.AccountPipeline': 300, },
        'LOG_ENABLED': False
    }

    def __init__(self, *args, **kwargs):
        super(DopagentSpider, self).__init__(*args, **kwargs)
        self.accounts_count = None
        self.account_counter = 0
        self.page_number = 1

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'AuthenticationFG.USER_PRINCIPAL': '',
                'AuthenticationFG.ACCESS_CODE': ''
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error('Login failed')
            return

        accounts_link = response.css(
            'a[id="Accounts"]::attr(href)').get()
        if accounts_link is not None:
            yield response.follow(accounts_link, callback=self.after_accounts_navigation)

    def after_accounts_navigation(self, response):
        if authentication_failed(response):
            self.logger.error('Accounts navigation failed')
            return

        agent_enquire_link = response.css(
            'a[id="Agent Enquire & Update Screen"]::attr(href)').get()
        if agent_enquire_link is not None:
            yield response.follow(agent_enquire_link, callback=self.after_agent_enquire_navigation)

    def after_agent_enquire_navigation(self, response):
        if authentication_failed(response):
            self.logger.error(
                'Agent Enquiry & Update Screen navigation failed')
            return

        if self.accounts_count is None:
            x = response.css('h2 span span::text').get()
            self.accounts_count = list(
                map(int, filter(lambda s: s.isdigit(), x.split(' '))))[-1]
            self.account_counter = self.account_counter if self.account_counter else 1


        if self.account_counter > self.accounts_count:
            return
        elif self.page_number != self.account_counter // 10:
            self.page_number = self.account_counter // 10
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    'CustomAgentRDAccountFG.AgentRDActSummaryAllListing_REQUESTED_PAGE_NUMBER': str(self.page_number)
                },
                clickdata={
                    'id': 'Action.AgentRDActSummaryAllListing.GOTO_PAGE__'},
                callback=self.after_agent_enquire_navigation
            )
        else:
            account_details = response.css(
                'table#SummaryList tr td a::attr(href)').getall()

            if (a := account_details[(self.account_counter - 1) % 10]) is not None:
                yield response.follow(a, callback=self.after_account_details_navigation)
                print(f'Scraped account {self.account_counter}')

            

    def after_account_details_navigation(self, response):
        if authentication_failed(response):
            self.logger.error('Account Details navigation failed')
            return

        def get_css(
            _id): return f'div p span[id="HREF_CustomAgentRDAccountFG.{_id}"]::text'

        account_loader = AccountLoader(item=AccountItem(), response=response)
        account_loader.add_css('account_no', get_css('ACCOUNT_NUMBER'))
        account_loader.add_css('name', get_css('ACCOUNT_NICKNAME'))
        account_loader.add_css('opening_date', get_css('RD_ACCOUNT_OPEN_DATE'))
        account_loader.add_css('denomination', get_css('RD_DESPOSIT_AMOUNT'))
        account_loader.add_css('total_deposit_amount',
                               get_css('RD_TOTAL_DESPOSIT_AMOUNT'))
        account_loader.add_css(
            'month_paid_upto', get_css('MONTH_PAID_UPTO_BASIC'))
        account_loader.add_css('next_installment_due_date',
                               get_css('NEXT_RD_INSTALLMENT_DATE'))
        account_loader.add_css('date_of_last_deposit',
                               get_css('DATE_OF_LAST_DEPOSIT'))
        account_loader.add_css('rebate_paid', get_css('REBATE'))
        account_loader.add_css('default_fee', get_css('DEFAULT_FEE'))
        account_loader.add_css('default_installments',
                               get_css('DEFAULT_INSTALLMENT'))
        account_loader.add_css('pending_installments',
                               get_css('PENDING_INSTALLMENT'))
        yield account_loader.load_item()

        self.account_counter += 1
        yield scrapy.FormRequest.from_response(
            response,
            clickdata={'name': 'Action.BACK_TO_ACCOUNT_LIST'},
            callback=self.after_agent_enquire_navigation
        )

import scraper.constants as CONST
import scraper.spiders.accounts.selectors as SELECT
import scraper.spiders.accounts.utils as utils
from scraper.utils import validate_response
from scrapy import FormRequest, Spider
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser


class AccountsSpider(Spider):
    name = 'accounts'
    start_urls = [CONST.DOPAGENT_BASE_URL]

    def __init__(self, agent_id='', password='', account_counter=0, *args, **kwargs):
        super(AccountsSpider, self).__init__(*args, **kwargs)

        self.total_accounts = None
        self.account_counter = account_counter
        self.page_number = 1
        self.agent_id = agent_id
        self.password = password

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formdata={
                CONST.LoginPage.AGENT_ID_INPUT: self.agent_id,
                CONST.LoginPage.PASSWORD_INPUT: self.password
            },
            callback=self.after_login
        )

    @validate_response
    def after_login(self, response):
        accounts_link = response.css(SELECT.ACCOUNTS_BUTTON__HREF).get()
        if accounts_link is not None:
            yield response.follow(accounts_link, callback=self.after_accounts_navigation)

    @validate_response
    def after_accounts_navigation(self, response):
        agent_enquire_link = response.css(
            SELECT.AGENT_ENQUIRE_AND_UPDATE_SCREEN__HREF).get()
        if agent_enquire_link is not None:
            yield response.follow(agent_enquire_link, callback=self.after_agent_enquire_navigation)

    @validate_response
    def after_agent_enquire_navigation(self, response):
        if self.total_accounts is None:
            self.total_accounts = utils.fetch_total_accounts(response)
            self.account_counter = self.account_counter if self.account_counter else 1

        if self.account_counter > self.total_accounts:
            return

        page, index = utils.account_counter_to_page_index(self.account_counter)
        if self.page_number != page:
            self.page_number = page
            yield self.goto_page_request(response, self.page_number, self.after_agent_enquire_navigation)
        else:
            all_accounts = response.css(SELECT.ACCOUNTS_LIST__HREF).getall()
            if (account_link := all_accounts[index]) is not None:
                yield response.follow(account_link, callback=self.after_account_details_navigation)
                print(f'Scraped account {self.account_counter}')

    @validate_response
    def after_account_details_navigation(self, response):
        yield utils.extract_account_item(response)

        self.account_counter += 1
        yield FormRequest.from_response(
            response,
            clickdata={'name':  CONST.AccountDetailPage.BACK_BUTTON},
            callback=self.after_agent_enquire_navigation
        )

    def goto_page_request(self, response, page_number, callback):
        return FormRequest.from_response(
            response,
            formdata={
                CONST.AccountsListPage.GOTO_PAGE_NUMBER_INPUT: str(page_number)},
            clickdata={'name': CONST.AccountsListPage.GOTO_PAGE_BUTTON},
            callback=callback
        )

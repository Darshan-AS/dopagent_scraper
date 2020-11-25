import scraper.constants as CONST
import scraper.spiders.accounts.selectors as SELECT
import scraper.spiders.accounts.utils as utils
from scraper.spiders.utils import fetch_total_accounts
from scraper.utils import validate_response
from scrapy import FormRequest, Spider
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser


class AccountsSpider(Spider):
    name = 'accounts'

    custom_settings = {
        'ITEM_PIPELINES': {'scraper.pipelines.AccountPipeline': 300},
        'LOG_ENABLED': True,
    }

    def __init__(self, account_counter=1, *args, **kwargs):
        super(AccountsSpider, self).__init__(*args, **kwargs)

        self.account_counter = account_counter

    @validate_response
    def parse(self, response, page_number=1, account_counter=None):
        total_accounts = fetch_total_accounts(response)
        account_counter = account_counter if account_counter else self.account_counter

        if account_counter > total_accounts:
            return

        page, index = utils.account_counter_to_page_index(account_counter)
        if page_number != page:
            yield self.goto_page_number_request(
                response, page, account_counter, self.parse
            )
        else:
            all_accounts = response.css(SELECT.ACCOUNTS_LIST__HREF).getall()
            if (account_link := all_accounts[index]) is not None:
                yield self.goto_account_detail_request(
                    response,
                    account_link,
                    page_number,
                    account_counter,
                    self.after_account_details_navigation,
                )
                print(f'Scraped account {account_counter}')

    @validate_response
    def after_account_details_navigation(self, response, **kwargs):
        yield utils.extract_account_item(response)

        yield FormRequest.from_response(
            response,
            clickdata={'name': CONST.AccountDetailPage.BACK_BUTTON},
            callback=self.parse,
            cb_kwargs=kwargs,
        )

    def goto_page_number_request(
        self, response, page_number, account_counter, callback
    ):
        return FormRequest.from_response(
            response,
            formdata={CONST.AccountsListPage.GOTO_PAGE_NUMBER_INPUT: str(page_number)},
            clickdata={'name': CONST.AccountsListPage.GOTO_PAGE_BUTTON},
            callback=callback,
            cb_kwargs={'page_number': page_number, "account_counter": account_counter},
        )

    def goto_account_detail_request(
        self, response, account_link, page_number, account_counter, callback
    ):
        return response.follow(
            account_link,
            callback=callback,
            cb_kwargs={
                'page_number': page_number,
                "account_counter": account_counter + 1,
            },
        )

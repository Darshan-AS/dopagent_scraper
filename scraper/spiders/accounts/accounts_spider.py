from scrapy import FormRequest, Spider

import scraper.constants as CONST
import scraper.spiders.accounts.selectors as SELECT
import scraper.spiders.accounts.utils as utils
from scraper.spiders.utils import fetch_total_accounts, stringify
from scraper.utils import validate_response


class AccountsSpider(Spider):
    name = 'accounts'

    custom_settings = {
        'ITEM_PIPELINES': {'scraper.pipelines.AccountPipeline': 0},
        'LOG_ENABLED': True,
    }

    def __init__(self, *args, account_counter=1, account_numbers=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.account_numbers = account_numbers
        self.account_counter = account_counter

    # pylint: disable=arguments-differ
    @validate_response
    def parse(self, response, **kwargs):
        if not self.account_numbers:
            yield from self.after_fetch_accounts_navigation(response)
            return

        yield FormRequest.from_response(
            response,
            formdata={
                CONST.AccountsListPage.ACCOUNT_NUMBER_SEARCH_BOX: stringify(
                    self.account_numbers
                )
            },
            clickdata={"name": CONST.AccountsListPage.FETCH_ACCOUNT_BUTTON},
            callback=self.after_fetch_accounts_navigation,
        )

    @validate_response
    def after_fetch_accounts_navigation(self, response, page_number=1, account_counter=None):
        total_accounts = fetch_total_accounts(response)
        account_counter = account_counter if account_counter else self.account_counter

        if account_counter > total_accounts:
            return

        page, index = utils.account_counter_to_page_index(account_counter)
        if page_number != page:
            yield self.goto_page_number_request(
                response, page, account_counter, self.after_fetch_accounts_navigation
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
            callback=self.after_fetch_accounts_navigation,
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

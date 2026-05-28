from scrapy import FormRequest, Spider, Request

import scraper.constants as CONST
import scraper.spiders.accounts.selectors as SELECT
import scraper.spiders.accounts.utils as utils
from scraper.spiders.utils import fetch_total_accounts, stringify
from scraper.utils import validate_response


class AccountsSpider(Spider):
    name = "accounts"

    custom_settings = {
        "ITEM_PIPELINES": {"scraper.pipelines.AccountPipeline": 0},
        "LOG_ENABLED": True,
    }

    def __init__(self, *args, url=None, referer=None, account_counter_start=1, account_counter_end=None, account_numbers=None, **kwargs):
        super().__init__(*args, **kwargs)

        if url:
            self.start_urls = [url]

        self.referer = referer
        self.account_numbers = account_numbers
        self.account_counter_start = int(account_counter_start) if account_counter_start else 1
        self.account_counter_end = int(account_counter_end) if account_counter_end else None

    def start_requests(self):
        for url in self.start_urls:
            headers = {}
            if self.referer:
                headers["Referer"] = self.referer
            yield Request(url, headers=headers, callback=self.parse)

    # pylint: disable=arguments-differ
    @validate_response
    def parse(self, response):
        # Check if we are already on the accounts list page
        if response.css(f"table#{CONST.AccountsListPage.ACCOUNTS_LIST_TABLE_ID}"):
            self.logger.info("On accounts list page.")
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
            return

        self.logger.error(
            f"Could not find account list table. On unknown page: {response.url}"
        )

    @validate_response
    def after_fetch_accounts_navigation(
        self, response, page_number=1, account_counter=None
    ):
        account_counter = account_counter if account_counter else self.account_counter_start

        total_accounts = fetch_total_accounts(response)
        self.logger.info(f"Total accounts found: {total_accounts}")

        if total_accounts == 0:
            self.logger.error(
                "Could not find total accounts. Check if the page structure is correct or if we are on the right page."
            )
            return

        if self.account_counter_end and account_counter > self.account_counter_end:
            self.logger.info(f"Finished scraping till specified end counter ({self.account_counter_end}).")
            return

        if account_counter > total_accounts:
            if response.css(
                f'input[name="{CONST.AccountsListPage.FETCH_MORE_ACCOUNTS_BUTTON}"]'
            ):
                self.logger.info(
                    f"Account {account_counter} > Total {total_accounts}. "
                    "Clicking Fetch More Accounts."
                )
                yield FormRequest.from_response(
                    response,
                    clickdata={
                        "name": CONST.AccountsListPage.FETCH_MORE_ACCOUNTS_BUTTON
                    },
                    callback=self.after_fetch_accounts_navigation,
                    cb_kwargs={
                        "page_number": page_number,
                        "account_counter": account_counter,
                    },
                )
            else:
                self.logger.info("Finished scraping all accounts.")
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
                self.logger.info(f"Scraped account {account_counter}")

    @validate_response
    def after_account_details_navigation(self, response, **kwargs):
        yield utils.extract_account_item(response)

        yield FormRequest.from_response(
            response,
            clickdata={"name": CONST.AccountDetailPage.BACK_BUTTON},
            callback=self.after_fetch_accounts_navigation,
            cb_kwargs=kwargs,
        )

    def goto_page_number_request(
        self, response, page_number, account_counter, callback
    ):
        return FormRequest.from_response(
            response,
            formdata={CONST.AccountsListPage.GOTO_PAGE_NUMBER_INPUT: str(page_number)},
            clickdata={"name": CONST.AccountsListPage.GOTO_PAGE_BUTTON},
            callback=callback,
            cb_kwargs={"page_number": page_number, "account_counter": account_counter},
        )

    def goto_account_detail_request(
        self, response, account_link, page_number, account_counter, callback
    ):
        return response.follow(
            account_link,
            callback=callback,
            cb_kwargs={
                "page_number": page_number,
                "account_counter": account_counter + 1,
            },
        )

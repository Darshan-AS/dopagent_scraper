import scraper.constants as CONST
import scraper.spiders.installments.selectors as SELECT
import scraper.spiders.installments.utils as utils
from scraper.spiders.utils import fetch_total_accounts
from scraper.utils import validate_response
from scrapy import FormRequest, Spider
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from enum import Enum


class PayMode(Enum):
    CASH = CONST.AccountsListPage.PAY_MODE_VALUE_CASH
    DOP_CHEQUE = CONST.AccountsListPage.PAY_MODE_VALUE_DOP_CHEQUE
    NON_DOP_CHEQUE = CONST.AccountsListPage.PAY_MODE_VALUE_NON_DOP_CHEQUE


class InstallmentsSpider(Spider):
    name = 'installments'

    def __init__(self, pay_mode=PayMode.CASH.name, account_numbers=[], *args, **kwargs):
        super(InstallmentsSpider, self).__init__(*args, **kwargs)

        self.pay_mode = PayMode[pay_mode]
        self.account_numbers = account_numbers

    @validate_response
    def parse(self, response):
        if not self.account_numbers:
            return

        return FormRequest.from_response(
            response,
            formdata={
                CONST.AccountsListPage.ACCOUNT_NUMBER_SEARCH_BOX:
                utils.stringify(self.account_numbers)
            },
            clickdata={'name': CONST.AccountsListPage.FETCH_ACCOUNT_BUTTON},
            callback=self.after_fetch_accounts_navigation
        )

    @validate_response
    def after_fetch_accounts_navigation(self, response, page_number=1):
        total_accounts = fetch_total_accounts(response)
        selected_data = utils.select_pay_mode_and_accounts(
            response,
            self.pay_mode
        )

        if total_accounts > page_number * CONST.ACCOUNTS_PER_PAGE:
            yield self.goto_page_number_request(
                response,
                page_number + 1,
                selected_data,
                self.after_fetch_accounts_navigation
            )
        else:
            yield self.save_installments_request(
                response,
                selected_data,
                self.after_save_installments_navigation
            )

    def after_save_installments_navigation(self, response):
        return FormRequest.from_response(
            response,
            clickdata={
                'name': CONST.InstallmentsPage.PAY_ALL_SAVED_INSTALLMENTS_BUTTON
            },
            callback=self.after_pay_saved_installment_navigation
        )

    def after_pay_saved_installment_navigation(self, response):
        yield utils.extract_auth_token_item(response)

    def goto_page_number_request(self, response, page_number, selected_data, callback):
        selected_data[
            CONST.AccountsListPage.GOTO_PAGE_NUMBER_INPUT
        ] = str(page_number)

        return FormRequest.from_response(
            response,
            formdata=selected_data,
            clickdata={'name': CONST.AccountsListPage.GOTO_PAGE_BUTTON},
            callback=callback,
            cb_kwargs={'page_number': page_number}
        )

    def save_installments_request(self, response, selected_data, callback):
        return FormRequest.from_response(
            response,
            formdata=selected_data,
            clickdata={'name': CONST.AccountsListPage.SAVE_ACCOUNTS_BUTTON},
            callback=callback
        )

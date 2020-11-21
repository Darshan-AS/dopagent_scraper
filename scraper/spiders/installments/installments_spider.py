import scraper.constants as CONST
from scraper.constants import InstallmentsPage
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

    def __init__(self, pay_mode=PayMode.CASH.name, accounts=[], *args, **kwargs):
        super(InstallmentsSpider, self).__init__(*args, **kwargs)

        self.pay_mode = PayMode[pay_mode]
        self.accounts = accounts
        self.account_installment_dict = {
            a['account_no']: a['no_of_installments'] for a in self.accounts
        }

    @validate_response
    def parse(self, response):
        if not self.accounts:
            return

        return FormRequest.from_response(
            response,
            formdata={
                CONST.AccountsListPage.ACCOUNT_NUMBER_SEARCH_BOX: utils.stringify(
                    self.account_installment_dict.keys()
                )
            },
            clickdata={'name': CONST.AccountsListPage.FETCH_ACCOUNT_BUTTON},
            callback=self.after_fetch_accounts_navigation,
        )

    @validate_response
    def after_fetch_accounts_navigation(self, response, page_number=1):
        total_accounts = fetch_total_accounts(response)
        selected_data = utils.select_pay_mode_and_accounts(response, self.pay_mode)

        if total_accounts > page_number * CONST.ACCOUNTS_PER_PAGE:
            yield self.goto_accounts_list_page_number_request(
                response,
                page_number + 1,
                selected_data,
                self.after_fetch_accounts_navigation,
            )
        else:
            yield self.save_installments_request(
                response,
                selected_data,
                self.after_save_installments_navigation,
            )

    def after_save_installments_navigation(
        self, response, page_number=1, modified=set()
    ):
        account_nos = utils.extract_installment_account_nos(response)
        for index, account_no in enumerate(account_nos):
            if (
                no_of_installment := self.account_installment_dict[account_no]
            ) > 1 and account_no not in modified:
                yield self.update_no_of_installments_request(
                    response,
                    index,
                    account_no,
                    no_of_installment,
                    page_number,
                    modified,
                    self.after_save_installments_navigation,
                )
                return

        total_accounts = fetch_total_accounts(response)
        if total_accounts > page_number * CONST.ACCOUNTS_PER_PAGE:
            yield self.goto_installments_list_page_number_request(
                response, page_number + 1, self.after_save_installments_navigation
            )
        else:
            yield self.pay_saved_installments_request(
                response, self.after_pay_saved_installment_navigation
            )

    def after_pay_saved_installment_navigation(self, response):
        yield utils.extract_reference_token_item(response)

    def goto_accounts_list_page_number_request(
        self, response, page_number, selected_data, callback
    ):
        selected_data[CONST.AccountsListPage.GOTO_PAGE_NUMBER_INPUT] = str(page_number)

        return FormRequest.from_response(
            response,
            formdata=selected_data,
            clickdata={'name': CONST.AccountsListPage.GOTO_PAGE_BUTTON},
            callback=callback,
            cb_kwargs={'page_number': page_number},
        )

    def save_installments_request(self, response, selected_data, callback):
        return FormRequest.from_response(
            response,
            formdata=selected_data,
            clickdata={'name': CONST.AccountsListPage.SAVE_ACCOUNTS_BUTTON},
            callback=callback,
        )

    def goto_installments_list_page_number_request(
        self, response, page_number, callback
    ):
        return FormRequest.from_response(
            response,
            formdata={CONST.InstallmentsPage.GOTO_PAGE_NUMBER_INPUT: str(page_number)},
            clickdata={'name': CONST.InstallmentsPage.GOTO_PAGE_BUTTON},
            callback=callback,
            cb_kwargs={'page_number': page_number},
        )

    def update_no_of_installments_request(
        self,
        response,
        index,
        account_no,
        no_of_installments,
        page_number,
        modified,
        callback,
    ):
        return FormRequest.from_response(
            response,
            formdata={
                CONST.InstallmentsPage.RADIO_BUTTON: str(index),
                CONST.InstallmentsPage.NO_OF_INSTALLMENTS_INPUT: str(
                    no_of_installments
                ),
            },
            clickdata={'name': CONST.InstallmentsPage.SAVE_NO_OF_INSTALLMENTS_BUTTON},
            callback=callback,
            cb_kwargs={
                "page_number": page_number,
                "modified": (modified | {account_no}),
            },
        )

    def pay_saved_installments_request(self, response, callback):
        return FormRequest.from_response(
            response,
            clickdata={
                'name': CONST.InstallmentsPage.PAY_ALL_SAVED_INSTALLMENTS_BUTTON
            },
            callback=callback,
        )

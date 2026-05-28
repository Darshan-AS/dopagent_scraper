import re

import scraper.constants as CONST
import scraper.spiders.installments.selectors as SELECT
from scraper.items import ReferenceTokenItem
from scraper.loaders import ReferenceTokenLoader


def select_pay_mode_and_accounts(response, pay_mode):
    checkboxes = response.css(SELECT.ACCOUNTS_LIST__CHECKBOXES)
    form_data = {
        checkbox.attrib["name"]: checkbox.attrib["value"] for checkbox in checkboxes
    }
    form_data[CONST.AccountsListPage.PAY_MODE_KEY] = pay_mode.value
    return form_data


def build_goto_page_form_data(selected_data, page_number):
    form_data = selected_data.copy()
    form_data[CONST.AccountsListPage.GOTO_PAGE_NUMBER_INPUT] = str(page_number)
    return form_data


def extract_reference_token_item(response):
    message = response.css(SELECT.MESSAGE__DIV).get()
    match = re.search("C\\d+", message)
    reference_number = match.group() if match else None

    reference_token_loader = ReferenceTokenLoader(
        item=ReferenceTokenItem(), response=response
    )
    reference_token_loader.add_value("reference_number", reference_number)
    return reference_token_loader.load_item()


def extract_installment_account_nos(response):
    account_nos = response.css(SELECT.INSTALLMENT_LIST_ACCOUNT_NOS).getall()
    return list(map(str.strip, account_nos))


def get_next_account_to_update(account_nos, account_installment_dict, modified_set):
    """
    Business logic to find the next account requiring more than 1 installment.
    """
    for index, account_no in enumerate(account_nos):
        no_of_installments = account_installment_dict.get(account_no, 1)
        if no_of_installments > 1 and account_no not in modified_set:
            return index, account_no, no_of_installments
    return None

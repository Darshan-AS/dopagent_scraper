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


def extract_reference_token_item(response):
    message = response.css(SELECT.MESSAGE__DIV).get()
    reference_number = re.search("C\\d+", message).group()

    reference_token_loader = ReferenceTokenLoader(
        item=ReferenceTokenItem(), response=response
    )
    reference_token_loader.add_value("reference_number", reference_number)
    return reference_token_loader.load_item()


def extract_installment_account_nos(response):
    account_nos = response.css(SELECT.INSTALLMENT_LIST_ACCOUNT_NOS).getall()
    return list(map(str.strip, account_nos))

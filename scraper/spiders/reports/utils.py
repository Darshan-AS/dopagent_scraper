from base64 import b64encode

import scraper.constants as CONST
from scraper.items import TransactionItem
from scraper.items.report_item import ReportItem
from scraper.loaders import TransactionLoader
from scraper.loaders.report_loader import ReportLoader


def extract_transaction_item(selector):
    def get_css(_id):
        return f'td span[id^="{_id}"]::text'

    transaction_loader = TransactionLoader(item=TransactionItem(), selector=selector)
    transaction_loader.add_css(
        'reference_number',
        get_css(CONST.ReportsPage.TRANSACTION_REFERENCE_NUMBER_ID_PREFIX),
    )
    transaction_loader.add_css(
        'account_number',
        get_css(CONST.ReportsPage.TRANSACTION_ACCOUNT_NUMBER_ID_PREFIX),
    )
    transaction_loader.add_css(
        'total_deposit_amount',
        get_css(CONST.ReportsPage.TRANSACTION_TOTAL_DEPOSIT_AMOUNT_ID_PREFIX),
    )
    transaction_loader.add_css(
        'no_of_installments',
        get_css(CONST.ReportsPage.TRANSACTION_NUMBER_OF_INSTALLMENTS_ID_PREFIX),
    )
    transaction_loader.add_css(
        'rebate',
        get_css(CONST.ReportsPage.TRANSACTION_REBATE_ID_PREFIX),
    )
    transaction_loader.add_css(
        'default_fee',
        get_css(CONST.ReportsPage.TRANSACTION_DEFAULT_FEE_ID_PREFIX),
    )
    transaction_loader.add_css(
        'status',
        get_css(CONST.ReportsPage.TRANSACTION_STATUS_ID_PREFIX),
    )
    transaction_loader.add_css(
        'last_created_date_and_time',
        get_css(CONST.ReportsPage.TRANSACTION_LAST_CREATED_DATE_AND_TIME_ID_PREFIX),
    )
    return transaction_loader.load_item()


def extract_report_item(response, reference_number, report_type, transaction_selectors):
    report_loader = ReportLoader(item=ReportItem())
    report_loader.add_value('reference_number', reference_number)
    report_loader.add_value('report_type', report_type)
    report_loader.add_value('base64_bytes', b64encode(response.body))
    for transaction_selector in transaction_selectors:
        report_loader.add_value(
            'transactions', extract_transaction_item(transaction_selector)
        )
    return report_loader.load_item()

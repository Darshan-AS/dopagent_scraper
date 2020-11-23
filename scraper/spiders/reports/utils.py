import scraper.constants as CONST
import scraper.spiders.reports.selectors as SELECT
from scraper.items import InstallmentItem
from scraper.loaders import InstallmentLoader


def extract_installment_item(selector):
    def get_css(_id):
        return f'td span[id^="{_id}"]::text'

    installment_loader = InstallmentLoader(item=InstallmentItem(), selector=selector)
    installment_loader.add_css(
        'reference_number',
        get_css(CONST.ReportsPage.INSTALLMENT_REFERENCE_NUMBER_ID_PREFIX),
    )
    installment_loader.add_css(
        'account_number',
        get_css(CONST.ReportsPage.INSTALLMENT_ACCOUNT_NUMBER_ID_PREFIX),
    )
    installment_loader.add_css(
        'total_deposit_amount',
        get_css(CONST.ReportsPage.INSTALLMENT_TOTAL_DEPOSIT_AMOUNT_ID_PREFIX),
    )
    installment_loader.add_css(
        'no_of_installments',
        get_css(CONST.ReportsPage.INSTALLMENT_NUMBER_OF_INSTALLMENTS_ID_PREFIX),
    )
    installment_loader.add_css(
        'rebate', get_css(CONST.ReportsPage.INSTALLMENT_REBATE_ID_PREFIX)
    )
    installment_loader.add_css(
        'default_fee', get_css(CONST.ReportsPage.INSTALLMENT_DEFAULT_FEE_ID_PREFIX)
    )
    installment_loader.add_css(
        'status', get_css(CONST.ReportsPage.INSTALLMENT_STATUS_ID_PREFIX)
    )
    installment_loader.add_css(
        'last_created_date_and_time',
        get_css(CONST.ReportsPage.INSTALLMENT_LAST_CREATED_DATE_AND_TIME_ID_PREFIX),
    )
    return installment_loader.load_item()

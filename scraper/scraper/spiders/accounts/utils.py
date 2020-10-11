import scraper.scraper.constants as CONST
import scraper.scraper.spiders.accounts.selectors as SELECT
from scraper.scraper.items import AccountItem
from scraper.scraper.loaders import AccountLoader


def account_counter_to_page_index(account_counter, accounts_per_page=CONST.ACCOUNTS_PER_PAGE):
    return account_counter // accounts_per_page, (account_counter - 1) % accounts_per_page


def fetch_total_accounts(response):
    total_accounts_text = response.css(SELECT.TOTAL_ACCOUNTS_TEXT).get()
    return list(map(int, filter(lambda s: s.isdigit(), total_accounts_text.split(' '))))[-1]


def extract_account_item(response):
    def get_css(_id): return f'div p span[id="{_id}"]::text'

    account_loader = AccountLoader(item=AccountItem(), response=response)
    account_loader.add_css('account_no',
                           get_css(CONST.AccountDetailPage.ACCOUNT_NUMBER_ID))
    account_loader.add_css('name',
                           get_css(CONST.AccountDetailPage.NAME_ID))
    account_loader.add_css('opening_date',
                           get_css(CONST.AccountDetailPage.OPENING_DATE_ID))
    account_loader.add_css('denomination',
                           get_css(CONST.AccountDetailPage.DENOMINATION_ID))
    account_loader.add_css('total_deposit_amount',
                           get_css(CONST.AccountDetailPage.TOTAL_DESPOSIT_AMOUNT_ID))
    account_loader.add_css('month_paid_upto',
                           get_css(CONST.AccountDetailPage.MONTH_PAID_UPTO_ID))
    account_loader.add_css('next_installment_due_date',
                           get_css(CONST.AccountDetailPage.NEXT_INSTALLMENT_DATE_ID))
    account_loader.add_css('date_of_last_deposit',
                           get_css(CONST.AccountDetailPage.LAST_DEPOSIT_DATE_ID))
    account_loader.add_css('rebate_paid',
                           get_css(CONST.AccountDetailPage.REBATE_ID))
    account_loader.add_css('default_fee',
                           get_css(CONST.AccountDetailPage.DEFAULT_FEE_ID))
    account_loader.add_css('default_installments',
                           get_css(CONST.AccountDetailPage.DEFAULT_INSTALLMENT_ID))
    account_loader.add_css('pending_installments',
                           get_css(CONST.AccountDetailPage.PENDING_INSTALLMENT_ID))
    return account_loader.load_item()

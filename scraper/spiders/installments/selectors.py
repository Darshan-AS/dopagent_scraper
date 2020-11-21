import scraper.constants as CONST

ACCOUNTS_LIST__CHECKBOXES = (
    f'table#{CONST.AccountsListPage.ACCOUNTS_LIST_TABLE_ID} tr td input[type=checkbox]'
)
MESSAGE__DIV = f'div#{CONST.AccountsListPage.MESSAGE_DISPLAY_TABLE_ID} div[role=alert]'
INSTALLMENT_LIST_ACCOUNT_NOS = (
    f'table tr td span[id^="{CONST.InstallmentsPage.ACCOUNT_NUMBER_ID_PREFIX}"]::text'
)

import scraper.constants as CONST

ACCOUNTS_LIST__HREF = (
    f"table#{CONST.AccountsListPage.ACCOUNTS_LIST_TABLE_ID} tr td a::attr(href)"
)

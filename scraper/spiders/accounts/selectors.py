import scraper.constants as CONST

ACCOUNTS_BUTTON__HREF = f'a[name="{CONST.MenuPage.ACCOUNTS_BUTTON}"]::attr(href)'
AGENT_ENQUIRE_AND_UPDATE_SCREEN__HREF = f'a[name="{CONST.MenuPage.AGENT_ENQIRE_AND_UPDATE_SCREEN_LINK}"]::attr(href)'
ACCOUNTS_LIST__HREF = 'table#SummaryList tr td a::attr(href)'
TOTAL_ACCOUNTS_TEXT = 'h2 span span::text'

import scraper.constants as CONST

FIRST_NAME__SPAN = f'div p span[id="{CONST.MenuPage.MESSAGE_TEXT_ID}"] span[id="{CONST.MenuPage.FIRST_NAME_TEXT_ID}"]::text'
LAST_NAME__SPAN = f'div p span[id="{CONST.MenuPage.MESSAGE_TEXT_ID}"] span[id="{CONST.MenuPage.LAST_NAME_TEXT_ID}"]::text'

DASHBOARD_BUTTON__HREF = f'a[name="{CONST.MenuPage.DASHBOARD_BUTTON}"]::attr(href)'
CHANGE_PASSWORD_BUTTON__HREF = (
    f'a[name="{CONST.MenuPage.CHANGE_PASSWORD_BUTTON}"]::attr(href)'
)
ACCOUNTS_BUTTON__HREF = f'a[name="{CONST.MenuPage.ACCOUNTS_BUTTON}"]::attr(href)'
AGENT_ENQUIRE_AND_UPDATE_SCREEN__HREF = (
    f'a[name="{CONST.MenuPage.AGENT_ENQIRE_AND_UPDATE_SCREEN_LINK}"]::attr(href)'
)
REPORTS__HREF = f'a[name="{CONST.MenuPage.REPORTS_LINK}"]::attr(href)'

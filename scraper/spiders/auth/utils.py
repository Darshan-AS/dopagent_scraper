import scraper.constants as CONST
import scraper.spiders.auth.selectors as SELECT
from scraper.items import AuthTokenItem
from scraper.loaders import AuthTokenLoader


def extract_auth_token_item(response):
    auth_token_loader = AuthTokenLoader(item=AuthTokenItem(), response=response)
    auth_token_loader.add_css(
        'dashboard_url',
        SELECT.DASHBOARD_BUTTON__HREF,
    )
    auth_token_loader.add_css(
        'change_password_uel',
        SELECT.CHANGE_PASSWORD_BUTTON__HREF,
    )
    auth_token_loader.add_css(
        'accounts_url',
        SELECT.ACCOUNTS_BUTTON__HREF,
    )
    auth_token_loader.add_css(
        'agent_enquire_screen_url',
        SELECT.AGENT_ENQUIRE_AND_UPDATE_SCREEN__HREF,
    )
    auth_token_loader.add_css(
        'reports_url',
        SELECT.REPORTS__HREF,
    )
    auth_token_loader.add_value(
        'referer_header',
        response.url,
    )
    return auth_token_loader.load_item()

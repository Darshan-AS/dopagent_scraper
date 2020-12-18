from scrapy import FormRequest, Spider

import scraper.constants as CONST
import scraper.spiders.auth.selectors as SELECT
import scraper.spiders.auth.utils as utils
from scraper.utils import validate_response


class AuthSpider(Spider):
    name = "auth"
    start_urls = [CONST.DOPAGENT_HOST]

    def __init__(self, *args, agent_id="", password="", **kwargs):
        super().__init__(*args, **kwargs)

        self.agent_id = agent_id
        self.password = password

    # pylint: disable=arguments-differ
    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formdata={
                CONST.LoginPage.AGENT_ID_INPUT: self.agent_id,
                CONST.LoginPage.PASSWORD_INPUT: self.password,
            },
            callback=self.after_login,
        )

    @validate_response
    def after_login(self, response):
        accounts_link = response.css(SELECT.ACCOUNTS_BUTTON__HREF).get()
        if accounts_link is not None:
            yield response.follow(
                accounts_link, callback=self.after_accounts_navigation
            )

    @validate_response
    def after_accounts_navigation(self, response):
        yield utils.extract_auth_token_item(response)

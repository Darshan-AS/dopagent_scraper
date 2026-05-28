from scrapy import FormRequest, Spider

import scraper.constants as CONST
import scraper.spiders.auth.selectors as SELECT
import scraper.spiders.auth.utils as utils
from scraper.utils import validate_response


class AuthSpider(Spider):
    name = "auth"
    start_urls = [CONST.DOPAGENT_HOST]

    custom_settings = {
        "LOG_ENABLED": True,
    }

    def __init__(self, *args, agent_id="", password="", **kwargs):
        super().__init__(*args, **kwargs)

        self.agent_id = agent_id
        self.password = password

    # pylint: disable=arguments-differ
    def parse(self, response):
        captcha_src = response.css(
            f"img#{CONST.LoginPage.CAPTCHA_IMAGE_ID}::attr(src)"
        ).get()
        if captcha_src:
            self.logger.info("CAPTCHA detected, attempting manual solution...")
            yield response.follow(
                captcha_src,
                callback=self.solve_captcha,
                meta={"login_response": response},
            )
        else:
            yield self.login_request(response)

    def solve_captcha(self, response):
        login_response = response.meta["login_response"]

        captcha_code = utils.resolve_manual_captcha(response.body, self.logger)

        return self.login_request(login_response, captcha_code)

    def login_request(self, response, captcha_code=None):
        formdata = {
            CONST.LoginPage.AGENT_ID_INPUT: self.agent_id,
            CONST.LoginPage.PASSWORD_INPUT: self.password,
        }

        if captcha_code:
            formdata[CONST.LoginPage.VERIFICATION_CODE_INPUT] = captcha_code

        request = FormRequest.from_response(
            response,
            formdata=formdata,
            clickdata={"name": CONST.LoginPage.LOG_IN_BUTTON},
            callback=self.after_login,
        )
        self.logger.info(f"Form Request Body: {request.body.decode()}")
        return request

    @validate_response
    def after_login(self, response):
        self.logger.info(f"Response URL after login: {response.url}")
        self.logger.info(f"Response Headers: {response.headers}")

        accounts_link = response.css(SELECT.ACCOUNTS_BUTTON__HREF).get()
        if accounts_link is not None:
            yield response.follow(
                accounts_link, callback=self.after_accounts_navigation
            )
        else:
            self.logger.error("Login failed or Accounts link not found.")
            # Log the message if present
            message = response.css(f"#{CONST.MenuPage.MESSAGE_TEXT_ID}::text").get()
            if message:
                self.logger.error(f"Portal message: {message}")

    @validate_response
    def after_accounts_navigation(self, response):
        enquire_url = response.css(SELECT.AGENT_ENQUIRE_AND_UPDATE_SCREEN__HREF).get()
        if enquire_url:
            self.logger.info(
                "Successfully navigated to Accounts screen. Extracting auth tokens."
            )
            yield utils.extract_auth_token_item(response, self.agent_id)
        else:
            self.logger.error("Enquire screen link not found.")
            yield utils.extract_auth_token_item(response, self.agent_id)

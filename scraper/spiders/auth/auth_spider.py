import os
import webbrowser
from scrapy import FormRequest, Spider

import scraper.constants as CONST
import scraper.spiders.auth.selectors as SELECT
import scraper.spiders.auth.utils as utils
import scraper.spiders.accounts.utils as utils_accounts
import scraper.spiders.accounts.selectors as SELECT_ACCOUNTS
from scraper.spiders.utils import fetch_total_accounts
from scraper.utils import validate_response


class AuthSpider(Spider):
    name = "auth"
    start_urls = [CONST.DOPAGENT_HOST]

    custom_settings = {
        "ITEM_PIPELINES": {"scraper.pipelines.AccountPipeline": 0},
        "LOG_ENABLED": True,
    }

    def __init__(self, *args, agent_id="", password="", account_counter=501, **kwargs):
        super().__init__(*args, **kwargs)

        self.agent_id = agent_id
        self.password = password
        self.account_counter = int(account_counter)

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
        captcha_path = "captcha.png"

        with open(captcha_path, "wb") as f:
            f.write(response.body)

        abs_path = os.path.abspath(captcha_path)
        self.logger.info(f"CAPTCHA image saved to {abs_path}")

        # Attempt to open the image automatically
        try:
            webbrowser.open(f"file://{abs_path}")
        except Exception:
            self.logger.warning("Could not open browser automatically.")

        captcha_code = input("Please enter the CAPTCHA code seen in the image: ")

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
            yield response.follow(
                enquire_url, 
                callback=self.after_enquire_navigation,
                cb_kwargs={"account_counter": self.account_counter}
            )
        else:
            self.logger.error("Enquire screen link not found.")
            yield utils.extract_auth_token_item(response, self.agent_id)

    @validate_response
    def after_enquire_navigation(self, response, page_number=1, account_counter=None):
        account_counter = (
            account_counter if account_counter is not None else self.account_counter
        )

        total_accounts = fetch_total_accounts(response)
        self.logger.info(f"Total accounts found: {total_accounts}")

        if account_counter > total_accounts:
            if response.css(
                f'input[name="{CONST.AccountsListPage.FETCH_MORE_ACCOUNTS_BUTTON}"]'
            ):
                self.logger.info(
                    f"Account {account_counter} > Total {total_accounts}. Clicking Fetch More Accounts."
                )
                yield FormRequest.from_response(
                    response,
                    clickdata={
                        "name": CONST.AccountsListPage.FETCH_MORE_ACCOUNTS_BUTTON
                    },
                    callback=self.after_enquire_navigation,
                    cb_kwargs={
                        "page_number": page_number,
                        "account_counter": account_counter,
                    },
                )
            else:
                self.logger.info("Finished scraping all accounts.")
            return

        page, index = utils_accounts.account_counter_to_page_index(account_counter)
        if page_number != page:
            self.logger.info(f"Navigating to page {page} for account {account_counter}")
            yield self.goto_page_number_request(
                response, page, account_counter, self.after_enquire_navigation
            )
        else:
            all_accounts = response.css(SELECT_ACCOUNTS.ACCOUNTS_LIST__HREF).getall()
            if index < len(all_accounts):
                account_link = all_accounts[index]
                self.logger.info(f"Scraping account {account_counter} (index {index} on page {page_number})")
                yield response.follow(
                    account_link,
                    callback=self.after_account_details_navigation,
                    cb_kwargs={
                        "page_number": page_number,
                        "account_counter": account_counter,
                    },
                )
            else:
                self.logger.error(f"Account index {index} not found on page {page_number}. Only {len(all_accounts)} accounts found.")

    @validate_response
    def after_account_details_navigation(self, response, page_number, account_counter):
        yield utils_accounts.extract_account_item(response)

        yield FormRequest.from_response(
            response,
            clickdata={"name": CONST.AccountDetailPage.BACK_BUTTON},
            callback=self.after_enquire_navigation,
            cb_kwargs={
                "page_number": page_number,
                "account_counter": account_counter + 1,
            },
        )

    def goto_page_number_request(
        self, response, page_number, account_counter, callback
    ):
        return FormRequest.from_response(
            response,
            formdata={CONST.AccountsListPage.GOTO_PAGE_NUMBER_INPUT: str(page_number)},
            clickdata={"name": CONST.AccountsListPage.GOTO_PAGE_BUTTON},
            callback=callback,
            cb_kwargs={"page_number": page_number, "account_counter": account_counter},
        )

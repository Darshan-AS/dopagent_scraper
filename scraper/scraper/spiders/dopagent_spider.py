import scrapy
from scrapy.utils.response import open_in_browser


def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass


class DopagentSpider(scrapy.Spider):
    name = 'dopagent'
    start_urls = ['https://dopagent.indiapost.gov.in/corp/AuthenticationController?FORMSGROUP_ID__=AuthenticationFG&__START_TRAN_FLAG__=Y&__FG_BUTTONS__=LOAD&ACTION.LOAD=Y&AuthenticationFG.LOGIN_FLAG=3&BANK_ID=DOP&AGENT_FLAG=Y']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'AuthenticationFG.USER_PRINCIPAL': '',
                'AuthenticationFG.ACCESS_CODE': ''
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error('Login failed')
            return
  
        accounts_navigation = response.css(
            'a[id="Accounts"]::attr(href)').get()
        if accounts_navigation is not None:
            yield response.follow(accounts_navigation, callback=self.after_accounts_navigation)

    def after_accounts_navigation(self, response):
        if authentication_failed(response):
            self.logger.error('Accounts navigation failed')
            return

  
        agent_enquire_navigation = response.css(
            'a[id="Agent Enquire & Update Screen"]::attr(href)').get()
        if agent_enquire_navigation is not None:
            yield response.follow(agent_enquire_navigation, callback=self.after_agent_enquire_navigation)

    def after_agent_enquire_navigation(self, response):
        if authentication_failed(response):
            self.logger.error(
                'Agent Enquiry & Update Screen navigation failed')
            return

       
        open_in_browser(response)
        # yield scrapy.FormRequest.from_response(
        #     response,
        #     clickdata={'id': 'Action.AgentRDActSummaryAllListing.GOTO_NEXT__'},
        #     callback=self.after_agent_enquire_navigation
        # )

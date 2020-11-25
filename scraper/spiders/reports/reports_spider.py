import scraper.constants as CONST
import scraper.spiders.reports.selectors as SELECT
import scraper.spiders.reports.utils as utils
from scraper.spiders.utils import fetch_total_accounts
from scraper.utils import validate_response
from scrapy import FormRequest, Spider
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from enum import Enum


class OutputType(Enum):
    PDF = CONST.ReportsPage.DOWNLOAD_FORMAT_SELECT_VALUE_PDF
    XLS = CONST.ReportsPage.DOWNLOAD_FORMAT_SELECT_VALUE_XLS


class ReportsSpider(Spider):
    name = 'reports'

    custom_settings = {
        'ITEM_PIPELINES': {'scraper.pipelines.TransactionPipeline': 400},
        'LOG_ENABLED': True,
    }

    def __init__(
        self, reference_number='', output_type=OutputType.PDF, *args, **kwargs
    ):
        super(ReportsSpider, self).__init__(*args, **kwargs)

        self.reference_number = reference_number
        self.output_type = OutputType[output_type]

    @validate_response
    def parse(self, response):
        if not self.reference_number:
            return

        return FormRequest.from_response(
            response,
            formdata={
                CONST.ReportsPage.REFERENCE_NUMBER_INPUT: self.reference_number,
                CONST.ReportsPage.STATUS_SELECT: CONST.ReportsPage.STATUS_SELECT_VALUE_SUCCESS,
            },
            clickdata={'name': CONST.ReportsPage.SEARCH_BUTTON},
            callback=self.after_search_reports_navigation,
        )

    @validate_response
    def after_search_reports_navigation(self, response, page_number=1):
        total_accounts = fetch_total_accounts(response)
        yield from map(
            utils.extract_transaction_item, response.css(SELECT.REPORT_LIST__ROWS)[2:-1]
        )

        if total_accounts > page_number * CONST.ACCOUNTS_PER_PAGE:
            yield self.goto_reports_page_number_request(
                response,
                page_number + 1,
                self.after_search_reports_navigation,
            )
        else:
            yield self.download_report_request(
                response,
                self.output_type.value,
                self.after_download_report_navigation,
            )

    def after_download_report_navigation(self, response):
        with open(
            f'./reports/{self.reference_number}.{str(self.output_type.name).lower()}',
            'wb',
        ) as f:
            f.write(response.body)

    def goto_reports_page_number_request(self, response, page_number, callback):
        return FormRequest.from_response(
            response,
            formdata={CONST.ReportsPage.GOTO_PAGE_NUMBER_INPUT: str(page_number)},
            clickdata={'name': CONST.ReportsPage.GOTO_PAGE_BUTTON},
            callback=callback,
            cb_kwargs={'page_number': page_number},
        )

    def download_report_request(self, response, download_format, callback):
        return FormRequest.from_response(
            response,
            formdata={CONST.ReportsPage.DOWNLOAD_FORMAT_SELECT: download_format},
            clickdata={'name': CONST.ReportsPage.DOWNLOAD_REPORT_BUTTON},
            callback=callback,
        )

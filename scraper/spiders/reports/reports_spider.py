from enum import Enum

from scrapy import FormRequest, Spider

import scraper.constants as CONST
import scraper.spiders.reports.selectors as SELECT
import scraper.spiders.reports.utils as utils
from scraper.spiders.utils import fetch_total_accounts
from scraper.utils import validate_response


class ReportType(Enum):
    PDF = CONST.ReportsPage.DOWNLOAD_FORMAT_SELECT_VALUE_PDF
    XLS = CONST.ReportsPage.DOWNLOAD_FORMAT_SELECT_VALUE_XLS


class ReportsSpider(Spider):
    name = 'reports'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ReportPipeline': 0,
        },
        'LOG_ENABLED': True,
    }

    def __init__(
        self, reference_number, *args, report_type=ReportType.PDF.name, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.reference_number = reference_number
        self.report_type = ReportType[report_type]

    # pylint: disable=arguments-differ
    @validate_response
    def parse(self, response):
        if not self.reference_number:
            return

        return FormRequest.from_response(
            response,
            # fmt: off
            formdata={
                CONST.ReportsPage.REFERENCE_NUMBER_INPUT:
                self.reference_number,
                CONST.ReportsPage.STATUS_SELECT:
                CONST.ReportsPage.STATUS_SELECT_VALUE_SUCCESS,
            },
            clickdata={'name': CONST.ReportsPage.SEARCH_BUTTON},
            callback=self.after_search_reports_navigation,
        )

    @validate_response
    def after_search_reports_navigation(
        self, response, page_number=1, transaction_selectors=None
    ):
        total_accounts = fetch_total_accounts(response)
        transaction_selectors = (
            transaction_selectors if transaction_selectors is not None else []
        )
        transaction_selectors.extend(response.css(SELECT.REPORT_LIST__ROWS)[2:-1])
        if total_accounts > page_number * CONST.ACCOUNTS_PER_PAGE:
            yield self.goto_reports_page_number_request(
                response,
                page_number + 1,
                transaction_selectors,
                self.after_search_reports_navigation,
            )
        else:
            yield self.download_report_request(
                response,
                self.report_type.value,
                transaction_selectors,
                self.after_download_report_navigation,
            )

    def after_download_report_navigation(self, response, transaction_selectors):
        yield utils.extract_report_item(
            response, self.reference_number, self.report_type, transaction_selectors
        )

    def goto_reports_page_number_request(
        self, response, page_number, transaction_selectors, callback
    ):
        return FormRequest.from_response(
            response,
            formdata={CONST.ReportsPage.GOTO_PAGE_NUMBER_INPUT: str(page_number)},
            clickdata={'name': CONST.ReportsPage.GOTO_PAGE_BUTTON},
            callback=callback,
            cb_kwargs={
                'page_number': page_number,
                'transaction_selectors': transaction_selectors,
            },
        )

    def download_report_request(
        self, response, download_format, transaction_selectors, callback
    ):
        return FormRequest.from_response(
            response,
            formdata={CONST.ReportsPage.DOWNLOAD_FORMAT_SELECT: download_format},
            clickdata={'name': CONST.ReportsPage.DOWNLOAD_REPORT_BUTTON},
            callback=callback,
            cb_kwargs={'transaction_selectors': transaction_selectors},
        )

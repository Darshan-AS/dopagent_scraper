from functools import wraps

from scrapy import Spider

import scraper.constants as CONST


# pylint: disable=inconsistent-return-statements
def validate_response(func):
    @wraps(func)
    def wrapper(self: Spider, response, *args, **kwargs):
        if response.status != CONST.SUCCESS_RESPONSE_STATUS:
            self.logger.error(f"Response not OK: {response.status} {response.url}")
        elif (
            response.headers.get(CONST.Headers.EXPIRED_KEY)
            != CONST.Headers.NOT_EXPIRED_VALUE
        ):
            self.logger.error(f"Session Timed Out: {response.url}")
        else:
            return func(self, response, *args, **kwargs)

    return wrapper

from functools import wraps

from scrapy import Spider

import scraper.scraper.constants as CONST


def validate_response(func):
    @wraps(func)
    def wrapper(self: Spider, response, *args, **kwargs):
        if response.status != CONST.SUCCESS_RESPONSE_STATUS:
            self.logger.error('Response not OK', response)
        elif response.headers[CONST.Headers.EXPIRED_KEY] != CONST.Headers.NOT_EXPIRED_VALUE:
            self.logger.error('Session Timed Out', response)
        else:
            return func(self, response, *args, **kwargs)
    return wrapper

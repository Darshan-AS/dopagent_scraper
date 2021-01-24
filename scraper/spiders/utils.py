import scraper.spiders.selectors as SELECT


def fetch_total_accounts(response):
    total_accounts_text = response.css(SELECT.TOTAL_ACCOUNTS_TEXT).get()
    return list(
        map(int, filter(lambda s: s.isdigit(), total_accounts_text.split(" ")))
    )[-1]


def stringify(account_numbers):
    return ",\n".join(map(str.strip, account_numbers))

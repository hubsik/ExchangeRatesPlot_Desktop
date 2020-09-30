from typing import List

PriceTypeOptionList: List[str] = [
    "Ask",
    "Bid",
]

CurrencyOptionList: List[str] = [
    "usd",
    "rub",
    "eur",
    "byn",
    "gel",
    "gbp"
]

CalendarIconPath = "calendar.png"

ChosenCurrency = CurrencyOptionList[0]

RequestAddress = "http://api.nbp.pl/api/exchangerates/rates/c/"\
                 + ChosenCurrency.lower() + \
                 "/2020-09-01/2020-09-15/?format=json"


class RequestParameters:
    def __init__(self, currency):
        self.Currency = currency

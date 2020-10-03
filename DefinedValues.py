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

ChosenCurrency = list(CurrencyOptionList[0])


def update_chosen_currency(curr: str):
    curr_list = list(curr)
    for i in range(len(curr)):
        ChosenCurrency[i] = curr_list[i]


def get_url():
    return "http://api.nbp.pl/api/exchangerates/rates/c/"+"".join(ChosenCurrency)+"/2020-09-01/2020-09-15/?format=json"

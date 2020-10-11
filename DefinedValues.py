from datetime import date, timedelta
from typing import List

PriceTypeOptionList: List[str] = [
    "Ask",
    "Bid",
]

CurrencyOptionList: List[str] = [
    "usd",
    "rub",
    "eur",
    "chf",
    "gbp"
]

ChosenCurrency = list(CurrencyOptionList[0])

ChosenStartDate = list((date.today() - timedelta(days=30)).strftime('%Y-%m-%d'))

ChosenEndDate = list(date.today().strftime('%Y-%m-%d'))


def update_chosen_currency(curr: str):
    ChosenCurrency.clear()
    curr_list = list(curr)
    for i in range(len(curr)):
        ChosenCurrency.append(curr_list[i])


def update_start_date(new_date):
    ChosenStartDate.clear()
    list_new_date = list(new_date)
    for i in range(len(new_date)):
        ChosenStartDate.append(list_new_date[i])


def update_end_date(new_date):
    ChosenEndDate.clear()
    list_new_date = list(new_date)
    for i in range(len(new_date)):
        ChosenEndDate.append(list_new_date[i])


def get_url():
    return "http://api.nbp.pl/api/exchangerates/rates/c/"+"".join(ChosenCurrency)+"/"+"".join(ChosenStartDate)+"/"+"".join(ChosenEndDate)+"/?format=json"

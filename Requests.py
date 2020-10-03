from DefinedValues import *
from ExchangeRates import *

import requests


def get_response(request_address):
    return requests.get(request_address)


def get_data_for_plot():
    exchange_rates = []
    print(get_url())
    print(''.join(ChosenCurrency))
    response = get_response(get_url())

    if 200 == response.status_code:
        json_response = response.json()
        exchange_rates = extract_rates(json_response['rates'])
    else:
        print("Error Code: " + str(response.status_code))

    return exchange_rates

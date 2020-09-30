class ExchangeRate:
    def __init__(self, date, bid, ask):
        self.Date = date
        self.Bid = bid
        self.Ask = ask


def extract_rates(obj):
    rates_arr = []

    # Extract every record of the list
    for item in obj:
        rates_arr.append(ExchangeRate(item['effectiveDate'], item['bid'], item['ask']))
    return rates_arr

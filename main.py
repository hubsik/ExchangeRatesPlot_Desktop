from UserInterface import *
from Requests import *


def main():
    exchange_rates = get_data_for_plot()

    if exchange_rates is not None:
        ui_display([rate.Date for rate in exchange_rates], [rate.Ask for rate in exchange_rates])


if __name__ == "__main__":
    main()

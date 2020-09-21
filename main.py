from typing import List

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import tkinter

PriceTypeOptionList: List[str] = [
"Ask",
"Bid",
]


class ExchangeRate:
    def __init__(self, date, bid, ask):
        self.Date = date
        self.Bid = bid
        self.Ask = ask


def main():
    exchange_rates = []
    response = requests.get('http://api.nbp.pl/api/exchangerates/rates/c/usd/2020-09-01/2020-09-15/?format=json')

    if 200 == response.status_code:
        json_response = response.json()
        exchange_rates = extract_rates(json_response['rates'])
    else:
        print("Error Code: " + str(response.status_code))

    if exchange_rates is not None:
        # Create window and set parameters
        gui_app = tkinter.Tk()
        gui_app.title("Exchange Rates")
        gui_app.state('zoomed')

        # Create frames
        frame_graph = tkinter.Frame(gui_app)
        frame_graph.pack(fill=tkinter.BOTH, expand=True)

        frame_settings = tkinter.Frame(gui_app)
        frame_settings.pack(fill=tkinter.X)

        # Create graph
        canvas = FigureCanvasTkAgg(add_graph(exchange_rates), frame_graph)
        canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        # Add Controls
        # Add Drop down list to chose Bid/Ask
        var_price_type = tkinter.StringVar(frame_settings)
        var_price_type.set(PriceTypeOptionList[0])

        opt_price_type = tkinter.OptionMenu(frame_settings, var_price_type, *PriceTypeOptionList)
        opt_price_type.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        #     tkinter.Button(frame_settings, text="Reset", command=show_button_callback)
        # button_aks.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        button_show = tkinter.Button(frame_settings, text="Reset", command=show_button_callback)
        button_show.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        button_waluta = tkinter.Button(frame_settings, text="Reset", command=show_button_callback)
        button_waluta.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        button_dataod = tkinter.Button(frame_settings, text="Reset", command=show_button_callback)
        button_dataod.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        button_datado = tkinter.Button(frame_settings, text="Reset", command=show_button_callback)
        button_datado.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        gui_app.mainloop()


def show_button_callback():
    print("Reset!!")


def extract_rates(obj):
    rates_arr = []

    # Extract every record of the list
    for item in obj:
        rates_arr.append(ExchangeRate(item['effectiveDate'], item['bid'], item['ask']))
    return rates_arr


def add_graph(arr: List[ExchangeRate]):
    # Add Graph
    fig = plt.figure(figsize=(5, 5), dpi=100)
    fig.subplots_adjust(bottom=0.2)

    a = fig.add_subplot(111)
    a.set_ylabel('PLN / 1USD')
    a.set_xlabel('Date')

    # Rotate x Axis labels
    for tick in a.get_xticklabels():
        tick.set_rotation(90)

    a.plot([rate.Date for rate in arr], [rate.Ask for rate in arr])
    return fig


if __name__ == "__main__":
    main()

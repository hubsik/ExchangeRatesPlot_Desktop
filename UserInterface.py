import tkinter

import matplotlib.pyplot as plt
import tkcalendar as tkc

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime
from Requests import *

fig = plt.figure(figsize=(5, 5), dpi=100)
fig.subplots_adjust(bottom=0.2)
graph = fig.add_subplot(111)


def ui_display(values_x, values_y):
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
    update_graph(values_x, values_y, CurrencyOptionList[0])

    canvas = FigureCanvasTkAgg(fig, frame_graph)
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, frame_graph)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # Add Controls
    # Add Drop down list and label to chose Bid/Ask
    label_price_type = tkinter.Label(frame_settings, text="Select Price type")
    label_price_type.pack(side=tkinter.LEFT)

    var_price_type = tkinter.StringVar(frame_settings)
    var_price_type.set(PriceTypeOptionList[0])

    opt_price_type = tkinter.OptionMenu(frame_settings, var_price_type, *PriceTypeOptionList)
    opt_price_type.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False, padx=(0, 10))

    # Add Drop down list and label to chose currency
    label_currency = tkinter.Label(frame_settings, text="Select currency: ")
    label_currency.pack(side=tkinter.LEFT)

    var_currency = tkinter.StringVar(frame_settings)
    var_currency.set(CurrencyOptionList[0])

    opt_currency = tkinter.OptionMenu(frame_settings, var_currency, *CurrencyOptionList)
    opt_currency.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False, padx=(0, 10))

    # Function to show calendar and pick date
    def show_calendar(btn: str):
        calendar_window = tkinter.Tk()
        calendar_window.title("Calendar")

        calendar = tkc.Calendar(calendar_window,
                                selectmode="day",
                                year=datetime.now().year,
                                month=datetime.now().month,
                                day=datetime.now().day,
                                date_pattern="y-mm-dd")

        def date_picked(event):
            if btn == "from":
                update_start_date(calendar.get_date())
                button_date_from["text"] = calendar.get_date()
            else:
                update_end_date(calendar.get_date())
                button_date_to["text"] = calendar.get_date()
            calendar_window.destroy()

        calendar.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False)
        calendar.bind('<<CalendarSelected>>', date_picked)

    # Add Calendar to pick start date
    label_date_from = tkinter.Label(frame_settings, text="Date from: ")
    label_date_from.pack(side=tkinter.LEFT)

    button_date_from = tkinter.Button(frame_settings, text="Pick a date", command=lambda: show_calendar("from"))
    button_date_from.pack(side=tkinter.LEFT, padx=(0, 10))

    # Add Calendar to pick end date
    label_date_to = tkinter.Label(frame_settings, text="Date to: ")
    label_date_to.pack(side=tkinter.LEFT)

    button_date_to = tkinter.Button(frame_settings, text="Pick a date", command=lambda: show_calendar("to"))
    button_date_to.pack(side=tkinter.LEFT, padx=(0, 10))

    # Add Button which will be trigger
    button_show = tkinter.Button(frame_settings, text="Show", command=lambda: show_button_callback(var_currency.get(), var_price_type.get()))
    button_show.pack(side=tkinter.LEFT, fill=tkinter.X, padx=(0, 10))

    def on_exit():
        gui_app.quit()

    gui_app.protocol("WM_DELETE_WINDOW", on_exit)
    gui_app.mainloop()


def update_graph(val_x, val_y, curr: str):
    # Update
    graph.set_ylabel('PLN / 1'+curr.upper())
    graph.set_xlabel('Date')

    # Rotate x axis
    for tick in graph.get_xticklabels():
        tick.set_rotation(90)

    graph.plot([datetime.strptime(x, '%Y-%m-%d').date() for x in val_x], val_y, color='green', marker='o', linestyle='dashed')


def show_button_callback(curr: str, price: str):
    data_for_y_axis = []

    # Update URL request
    update_chosen_currency(curr)

    # Get new data
    exchange_rates = get_data_for_plot()

    # Get new new operation type
    if price == PriceTypeOptionList[0]:
        data_for_y_axis = [rate.Ask for rate in exchange_rates]
    else:
        data_for_y_axis = [rate.Bid for rate in exchange_rates]

    # Clear, update, show new graph
    clear_graph()
    update_graph([rate.Date for rate in exchange_rates], data_for_y_axis, curr)
    update_figure()


def clear_graph():
    graph.clear()


def update_figure():
    fig.canvas.draw()

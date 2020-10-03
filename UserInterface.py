import tkinter
import datetime
from tkinter import OptionMenu

import matplotlib.pyplot as plt
import tkcalendar as tkc

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Requests import *

fig = plt.figure(figsize=(5, 5), dpi=100)
fig.subplots_adjust(bottom=0.2)
graph = fig.add_subplot(111)


def ui_display(values_x, values_y):
    # Create window and set parameters
    gui_app = tkinter.Tk()
    gui_app.title("Exchange Rates")
    #gui_app.state('zoomed')

    # Create frames
    frame_graph = tkinter.Frame(gui_app)
    frame_graph.pack(fill=tkinter.BOTH, expand=True)

    frame_settings = tkinter.Frame(gui_app)
    frame_settings.pack(fill=tkinter.X)

    # Create graph
    update_graph(values_x, values_y, CurrencyOptionList[0])

    canvas = FigureCanvasTkAgg(fig, frame_graph)
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    # Add Controls
    # Add Drop down list and label to chose Bid/Ask
    label_price_type = tkinter.Label(frame_settings, text="Select price type: ")
    label_price_type.pack(side=tkinter.LEFT)

    var_price_type = tkinter.StringVar(frame_settings)
    var_price_type.set(PriceTypeOptionList[0])

    opt_price_type = tkinter.OptionMenu(frame_settings, var_price_type, *PriceTypeOptionList)
    opt_price_type.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False)

    # Add Drop down list and label to chose currency
    label_currency = tkinter.Label(frame_settings, text="Select currency: ")
    label_currency.pack(side=tkinter.LEFT)

    var_currency = tkinter.StringVar(frame_settings)
    var_currency.set(CurrencyOptionList[0])

    opt_currency = tkinter.OptionMenu(frame_settings, var_currency, *CurrencyOptionList)
    opt_currency.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False)

    # Add Calendar to pick start date
    label_date_from = tkinter.Label(frame_settings, text="Date from: ")
    label_date_from.pack(side=tkinter.LEFT)

    # Need to google error which is generated, 'image' is not working properly
    # photo = tkinter.PhotoImage(file=CalendarIconPath).subsample(10, 10)
    # button_date_from = tkinter.Button(frame_settings, text="Pick a date", image=photo, command=show_calendar)
    button_date_from = tkinter.Button(frame_settings, text="Pick a date", command=show_calendar)

    # Added only to prevent from being garbage collected
    # button_date_from.image = photo
    button_date_from.pack(side=tkinter.LEFT)

    button_show = tkinter.Button(frame_settings, text="Show", command=lambda: show_button_callback(var_currency.get(), var_price_type.get()))
    button_show.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

    gui_app.mainloop()


def update_graph(val_x, val_y, curr: str):
    # Update
    graph.set_ylabel('PLN / 1'+curr.upper())
    graph.set_xlabel('Date')
    update_axis()
    graph.plot(val_x, val_y)


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


def update_axis():
    # Rotate x Axis labels
    for tick in graph.get_xticklabels():
        tick.set_rotation(90)


# def add_option_type_controls(fr: tkinter.Frame):


# def add_currency_controls(fr: tkinter.Frame):
#     label_currency = tkinter.Label(fr, text="Select currency: ")
#     label_currency.pack(side=tkinter.LEFT)
#
#     var_currency = tkinter.StringVar(fr)
#     var_currency.set(CurrencyOptionList[0])
#
#     opt_currency = tkinter.OptionMenu(fr, var_currency, *CurrencyOptionList)
#     opt_currency.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False)


# def add_date_from_controls(fr: tkinter.Frame):
#     label_date_from = tkinter.Label(fr, text="Date from: ")
#     label_date_from.pack(side=tkinter.LEFT)
#
#     # Need to google error which is generated, 'image' is not working properly
#     # photo = tkinter.PhotoImage(file=CalendarIconPath).subsample(10, 10)
#     # button_date_from = tkinter.Button(fr, text="Pick a date", image=photo, command=show_calendar)
#     button_date_from = tkinter.Button(fr, text="Pick a date", command=show_calendar)
#
#     # Added only to prevent from being garbage collected
#     # button_date_from.image = photo
#     button_date_from.pack(side=tkinter.LEFT)


def show_calendar():
    calendar_window = tkinter.Tk()
    calendar_window.title("Calendar")

    widgets_list = calendar_window.pack_slaves()
    widgets_list = set(widgets_list)

    if tkc.Calendar not in widgets_list:
        calendar = tkc.Calendar(calendar_window,
                                selectmode="day",
                                year=datetime.datetime.now().year,
                                month=datetime.datetime.now().month,
                                day=datetime.datetime.now().day,
                                date_pattern="y-mm-dd")
        calendar.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False)

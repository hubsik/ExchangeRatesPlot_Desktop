import tkinter
import datetime

import matplotlib.pyplot as plt
import tkcalendar as tkc

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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

    # Add Calendar to pick start date
    label_date_from = tkinter.Label(frame_settings, text="Date from: ")
    label_date_from.pack(side=tkinter.LEFT)

    # Need to google error which is generated, 'image' is not working properly
    # photo = tkinter.PhotoImage(file=CalendarIconPath).subsample(10, 10)
    # button_date_from = tkinter.Button(frame_settings, text="Pick a date", image=photo, command=show_calendar)
    button_date_from = tkinter.Button(frame_settings, text="Pick a date", command=show_calendar)

    # Added only to prevent from being garbage collected
    # button_date_from.image = photo
    button_date_from.pack(side=tkinter.LEFT, padx=(0, 10))

    button_show = tkinter.Button(frame_settings, text="Show", command=lambda: show_button_callback(var_currency.get(), var_price_type.get()))
    button_show.pack(side=tkinter.LEFT, fill=tkinter.X, padx=(0, 10))

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

        def date_picked(event):
            print(calendar.get_date())
            update_end_date(calendar.get_date())
            calendar_window.destroy()

        calendar.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False)
        calendar.bind('<<CalendarSelected>>', date_picked)



import tkinter
import datetime

import PIL
import matplotlib.pyplot as plt
import tkcalendar as tkc

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DefinedValues import *


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
    update_graph(values_x, values_y)
    update_axis()
    canvas = FigureCanvasTkAgg(fig, frame_graph)
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    # Add Controls
    # Add Drop down list and label to chose Bid/Ask
    add_option_type_controls(frame_settings)

    # Add Drop down list and label to chose currency
    add_currency_controls(frame_settings)

    # Add Calendar to pick start date
    add_date_from_controls(frame_settings)

    button_show = tkinter.Button(frame_settings, text="Show", command=show_button_callback)
    button_show.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

    gui_app.mainloop()


def update_graph(val_x, val_y):
    # Update
    graph.set_ylabel('PLN / 1USD')
    graph.set_xlabel('Date')
    graph.plot(val_x, val_y)


def show_button_callback():
    clear_graph()
    update_graph([1, 2, 3], [1, 1, 1])
    update_figure()


def clear_graph():
    graph.clear()


def update_figure():
    fig.canvas.draw()


def update_axis():
    # Rotate x Axis labels
    for tick in graph.get_xticklabels():
        tick.set_rotation(90)


def add_option_type_controls(fr: tkinter.Frame):
    label_price_type = tkinter.Label(fr, text="Select price type: ")
    label_price_type.pack(side=tkinter.LEFT)

    var_price_type = tkinter.StringVar(fr)
    var_price_type.set(PriceTypeOptionList[0])

    opt_price_type = tkinter.OptionMenu(fr, var_price_type, *PriceTypeOptionList)
    opt_price_type.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False)


def add_currency_controls(fr: tkinter.Frame):
    label_currency = tkinter.Label(fr, text="Select currency: ")
    label_currency.pack(side=tkinter.LEFT)

    var_currency = tkinter.StringVar(fr)
    var_currency.set(CurrencyOptionList[0])

    opt_currency = tkinter.OptionMenu(fr, var_currency, *CurrencyOptionList)
    opt_currency.pack(side=tkinter.LEFT, fill=tkinter.X, expand=False)


def add_date_from_controls(fr: tkinter.Frame):
    label_date_from = tkinter.Label(fr, text="Date from: ")
    label_date_from.pack(side=tkinter.LEFT)

    # Need to google error which is generated, 'image' is not working properly
    # photo = tkinter.PhotoImage(file=CalendarIconPath).subsample(10, 10)
    # button_date_from = tkinter.Button(fr, text="Pick a date", image=photo, command=show_calendar)
    button_date_from = tkinter.Button(fr, text="Pick a date", command=show_calendar)

    # Added only to prevent from being garbage collected
    # button_date_from.image = photo
    button_date_from.pack(side=tkinter.LEFT)


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

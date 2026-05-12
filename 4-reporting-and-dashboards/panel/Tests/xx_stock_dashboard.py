import panel as pn
import yfinance as yf
import pandas as pd
import hvplot.pandas
from bokeh.models import DatetimeTickFormatter
import time

pn.extension()

def get_data():
    df = pd.read_csv('google_stock_data.csv')
    return df

def update():
    df = get_data()
    print("updating...")
    markdonw_panel.object = f"## Google Stock Price Live Update\n\nLast Updated: {df['Datetime'].iloc[-1]}"
    plot = df.hvplot.line(x='Datetime', y='Close', title='Google Stock Price', width=800, height=400)
    plot.xformatter = DatetimeTickFormatter(minutes=['%H:%M'], hours=['%H:%M'], days=['%m/%d'], months=['%m/%d'], years=['%Y'])
    plot_panel.object = plot

df = get_data()
plot_panel = pn.pane.HoloViews(df.hvplot.line(x='Datetime', y='Close', title='Google Stock Price', width=800, height=400))

markdonw_panel = pn.pane.Markdown("--# Google Stock Price Live Update")

dashboard = pn.Column(
    markdonw_panel,
    plot_panel
)

# Add periodic callback to update the plot every minute (60000 milliseconds)
pn.state.add_periodic_callback(update, 5000)

dashboard.servable()
pn.serve(dashboard)

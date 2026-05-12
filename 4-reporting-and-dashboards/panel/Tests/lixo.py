import panel as pn
import time

# Initialize Panel
pn.extension()

# Create a Text widget
text_widget = pn.widgets.StaticText(name='Current Time', value='')

# Define a function to update the widget
def update_widget():
    text_widget.value = time.strftime('%Y-%m-%d %H:%M:%S')

# Schedule the update function to be called every 5 seconds
callback = pn.state.add_periodic_callback(update_widget, period=1000)

# Create a layout to display the widget
layout = pn.Column(
    text_widget,
    callback
).servable()

# Serve the app
#pn.serve(layout)

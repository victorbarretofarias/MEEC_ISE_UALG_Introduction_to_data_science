import panel as pn
pn.extension()

slider = pn.widgets.FloatSlider(name='Slider', start=0, end=10, step=0.1)
text_input = pn.widgets.TextInput(name='Text Input', placeholder='Enter text here...')
checkbox = pn.widgets.Checkbox(name='Checkbox')

row = pn.Row(slider, text_input, checkbox)
tabs = pn.Tabs( ('Slider', slider), ('Text Input', text_input), ('Checkbox', checkbox ), background='lightgray')

pn.Column(row, tabs).servable()
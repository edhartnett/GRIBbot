import panel as pn
from time import sleep
import altair as alt
import vega_datasets

# pn.extension("vega", sizing_mode="stretch_width")

# # Lets show some interactivity
# slider = pn.widgets.IntSlider(start=0, end=10, margin=(10,10,25,10))
# settings = pn.WidgetBox(slider, slider.param.value)
# settings

# # Lets layout things
# tabs = pn.layout.Tabs(
#     pn.pane.Markdown("Hello", name="Tab 1"),
#     name="Output",
#     sizing_mode="stretch_both",
#     dynamic=True,
#     closable=True
# )
# tabs

# layout = pn.Column(
#     "## Panel in VS Code",
#     slider,
#     tabs
# )
# layout

# # Lets explore in a new window
# layout.show()



pn.extension()
#pn.extension("vega", sizing_mode="stretch_width")
def get_response(contents, user, instance):
    if "turbine" in contents.lower():
        response = "A wind turbine converts wind energy into electricity."
    else:
        response = "Sorry, I don't know."
    sleep(1)
    return response

chat_bot = pn.chat.ChatInterface(callback=get_response, max_height=500)
chat_bot.send("Ask me what a wind turbine is", user="Assistant", respond=False)
chat_bot.show()
chat_bot.servable()
import panel as pn

import altair as alt
import vega_datasets

pn.extension("vega", sizing_mode="stretch_width")

# Lets show some interactivity
slider = pn.widgets.IntSlider(start=0, end=10, margin=(10,10,25,10))
settings = pn.WidgetBox(slider, slider.param.value)
settings

# Lets layout things
tabs = pn.layout.Tabs(
    pn.pane.Markdown("Hello", name="Tab 1"),
    name="Output",
    sizing_mode="stretch_both",
    dynamic=True,
    closable=True
)
tabs

layout = pn.Column(
    "## Panel in VS Code",
    slider,
    tabs
)
layout

# Lets explore in a new window
layout.show()

# Lets add a plot
def create_altair_plot(size=3):
    source = vega_datasets.data.seattle_weather()

    line = alt.Chart(source).mark_line(
        color='red',
        size=size
    ).transform_window(
        rolling_mean='mean(temp_max)',
        frame=[-15, 15]
    ).encode(
        x='date:T',
        y='rolling_mean:Q'
    )

    points = alt.Chart(source).mark_point().encode(
        x='date:T',
        y=alt.Y('temp_max:Q',
                axis=alt.Axis(title='Max Temp'))
    )

    return (points + line).properties(height=500, width="container")

altair_plot = create_altair_plot()
tabs.append(pn.panel(altair_plot, name="Altair Plot"))

# Lets add an interactive plot
create_altair_plot_interactive=pn.bind(create_altair_plot, size=slider)
tabs[-1]=pn.panel(create_altair_plot_interactive, name="Interactive AP")

# Lets save it as an interactive html report that you can email to your stakeholders
tabs.dynamic=False
layout.save("report.html", embed=True, max_opts=10)
import json
import pygal
from pygal.style import Style
import pandas as pd


def top_5_customers():
    df = pd.read_csv("sales_data_sample.csv", encoding='unicode_escape')

    custom_style = Style(
        plot_background='rgb(255,255,255,1)',
        background='rgb(255,255,255,1)',

    # Monospaced font is highly encouraged
    font_family=('sans-serif'),

    opacity=0.8,
    opacity_hover=1,

    label_font_size=12,
    major_label_font_size=12,
    value_font_size=18,
    value_label_font_size=12,
    tooltip_font_size=16,
    title_font_size=18,
    legend_font_size=16,
    no_data_font_size=66,

    # Guide line dash array style
    guide_stroke_dasharray='none',
    major_guide_stroke_dasharray='none',
    guide_stroke_color='black',
    major_guide_stroke_color='black',

    stroke_opacity='1',
    stroke_width='20',
    stroke_opacity_hover='1',
    stroke_width_hover='4',

    transition='400ms ease-in',
    colors=('#0f6987', '#bc5190', '#ffa600', '#3b4d80', '#E89B53')
)

    customer_revenue = df.groupby(['CUSTOMERNAME'])['SALES'].sum().reset_index()
    customer_revenue = customer_revenue.to_json(orient='values')
    data = json.loads(customer_revenue)
    data.sort(key=lambda x: x[1], reverse=True)
    # print(data)

    bar_chart = pygal.Bar(style=custom_style,
                      value_formatter=lambda x: '${}'.format(x))
    bar_chart.formatter = lambda x: '${:.2f}'.format(x)

    value = 0

    for x in data:
        if value == 5:
            break
        else:
            bar_chart.add(str(x[0]), x[1])
            value += 1

    return bar_chart

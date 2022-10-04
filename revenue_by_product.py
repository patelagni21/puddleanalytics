
import json
import pygal
from pygal.style import Style
import pandas as pd


def revenue_by_product(filename):
    print(filename)
    df = pd.read_csv(filename, sep=";", encoding = 'ISO-8859-1')

    custom_style = Style(
        plot_background = 'rgb(255,255,255,1)',
        background = 'rgb(255,255,255,1)',

        # Monospaced font is highly encouraged
        font_family = ('sans-serif'),
        
        opacity = 0.7,
        opacity_hover = 1,

        label_font_size = 12,
        major_label_font_size = 12,
        value_font_size = 18,
        value_label_font_size = 12,
        tooltip_font_size = 16,
        title_font_size = 18,
        legend_font_size = 16,
        no_data_font_size = 66,

        # Guide line dash array style
        guide_stroke_dasharray = 'none',
        major_guide_stroke_dasharray = 'none',
        guide_stroke_color = 'black',
        major_guide_stroke_color = 'black',
        
        stroke_opacity = '1',
        stroke_width = '20',
        stroke_opacity_hover = '1',
        stroke_width_hover = '4',

        transition = '400ms ease-in',
        colors = ( '#0f6987', '#bc5190', '#ffa600', '#3b4d80', '#E89B53')
        )

    productRevenue= df.groupby(['PRODUCTLINE'])['SALES'].sum().reset_index()
    sum = productRevenue.sum()
    js = productRevenue.to_json(orient='records')
    data = json.loads(js)


    pie_chart=pygal.Pie(half_pie=True, inner_radius=0.4, style=custom_style)
    percent_formatter = lambda x: '{:.2f}%'.format(x)
    pie_chart.value_formatter = percent_formatter
    # pie_chart.title='Revenue of Different Products (in %)'
    for i in data:
        pie_chart.add(str(i['PRODUCTLINE']), i['SALES']/int(sum[1])*100)


    return pie_chart



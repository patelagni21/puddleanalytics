import json
import pygal
from pygal.style import Style
import pandas as pd


def average_sales(filename):
    df = pd.read_csv(filename, sep=";", encoding = 'ISO-8859-1')

    custom_style = Style(
        plot_background = 'rgb(255,255,255,1)',
        background = 'transparent',

        # Monospaced font is highly encouraged
        font_family = ('sans-serif'),

        opacity = 0.8,
        opacity_hover = 1,
        value_font_size = 40,
        label_colors=('white',),
        value_colors=('white',),

        label_font_size = 12,
        major_label_font_size = 12,
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

    totalSales = df['SALES'].sum()

    barChart = pygal.Bar(
        print_values = True,
        print_labels = True,
        height=400, 
        include_x_axis=False,
        show_y_guides = False,
        style=custom_style)
    barChart.title = 'Sales per Fiscal Year'
    barChart.y_title = 'Sales in $'
    barChart.add('', [{'value':totalSales/df['SALES'].size, 'label':'Average Spent'}])
    barChart.value_formatter =lambda x: '${:.2f}'.format(x)

    barChart.render_in_browser()

average_sales()
import json
import pygal
from pygal.style import Style
import pandas as pd
from collections import defaultdict
from datetime import datetime
from csv import reader
import numpy as np


def average_sales_per_month(filename):
    df = pd.read_csv(filename, sep=";", encoding = 'ISO-8859-1')

    custom_style = Style(
        plot_background = 'rgb(255,255,255,1)',
        background = 'rgb(255,255,255,1)',

        # Monospaced font is highly encouraged
        font_family = ('Sans Serif'),
        

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

    date_list=[]

    for ind in df.index:
        if datetime(df['YEAR_ID'][ind], df['MONTH_ID'][ind], 1) not in date_list:
            date_list.append(datetime(df['YEAR_ID'][ind], df['MONTH_ID'][ind], 1))
            


    average_revenue=df.groupby(['YEAR_ID','MONTH_ID'])['SALES'].mean().reset_index()
    js = average_revenue.to_json(orient='values')
    data = json.loads(js)

    sales_list=[]

    for x in data:
        sales_list.append(x[2])



    date_list=sorted(date_list)




    line_chart=pygal.Line(x_label_rotation=80, style=custom_style, opacity=0, show_y_guides=False, show_x_guides=False, include_x_axis=False,include_y_axis=False,value_formatter=lambda x: '${:.2f}'.format(x))
    line_chart.title='Average sale per month in $'
    line_chart.formatter= lambda x: '${:.2f}'.format(x)
    line_chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), date_list)



    line_chart.add('Revenue', sales_list)

        # line_chart.render_in_browser()
    return line_chart


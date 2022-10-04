"""
Created on Mon June 6

@author: jairad26
"""

import json
import pygal
from pygal.style import Style
import pandas as pd
from collections import defaultdict

def month_rev(filename):
    df = pd.read_csv(filename, sep=";", encoding = 'ISO-8859-1')

    custom_style = Style(
        plot_background = 'rgb(255,255,255,1)',
        background = 'rgb(255,255,255,1)',

        # Monospaced font is highly encouraged
        font_family = ('sans-serif'),
        

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

    quarterly_revenue=df.groupby(['YEAR_ID','MONTH_ID'])['SALES'].sum().reset_index()
    js = quarterly_revenue.to_json(orient='values')
    data = json.loads(js)


    dict=defaultdict(list)


    for x in data:
        dict[x[0]].append(x[2])

    month_list = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
    line_chart=pygal.Line(
        dots_size=4,
        stroke_style={'width': 3,'linecap':'round','linejoin':'round'},
        include_x_axis=True,
        show_y_guides = False, 
        show_x_guides = True, 
        style=custom_style, 
        value_formatter=lambda x: '${:.2f}'.format(x)
        )
    line_chart.formatter=lambda x: '${:.2f}'.format(x)
    line_chart.title='Revenue by Month per Year'
    line_chart.y_title = 'Sales in $'
    line_chart.x_labels=[x for x in month_list]
    for x in dict:
        line_chart.add(str(x),dict[x])


    return line_chart

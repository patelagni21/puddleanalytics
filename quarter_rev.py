#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 14:06:05 2021

@author: alexortiz
"""

import json
from pygal.style import Style

def quarter_rev(filename):
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
    #TODO figure out how to make pop-up window opaque
    import pandas as pd
    from collections import defaultdict

    df = pd.read_csv(filename, sep=";", encoding = 'ISO-8859-1')
    pd.options.mode.chained_assignment = None

    #Get all 4 quarter sales from each year starting with 2003:
    import pygal


    df['Quarter'] = df['MONTH_ID'].copy()
    for x in range(df['Quarter'].size):
        if((df['Quarter'][x] == 1) | (df['Quarter'][x] == 2) | (df['Quarter'][x] == 3)):
            df['Quarter'][x] = 1
        elif((df['Quarter'][x] == 4) | (df['Quarter'][x] == 5) | (df['Quarter'][x] == 6)):
            df['Quarter'][x] = 2
        elif((df['Quarter'][x] == 7) | (df['Quarter'][x] == 8) | (df['Quarter'][x] == 9)):
            df['Quarter'][x] = 3
        elif((df['Quarter'][x] == 10) | (df['Quarter'][x] == 11)| (df['Quarter'][x] == 12)):
            df['Quarter'][x] = 4
        else:
            df['Quarter'][x] = None
            

    quarterly_revenue=df.groupby(['YEAR_ID','Quarter'])['SALES'].sum().reset_index()
    js = quarterly_revenue.to_json(orient='values')
    data = json.loads(js)

    dict=defaultdict(list)

    for x in data:
        dict[x[0]].append(x[2])

    line_chart=pygal.Line(
    dots_size=4,
    stroke_style={'width': 3,'linecap':'round','linejoin':'round'},
    include_x_axis=True,
    show_y_guides = False, 
    show_x_guides = True, 
    style=custom_style,
    value_formatter=lambda x: '${:.2f}'.format(x))
    line_chart.title='Revenue by Quarter per Year'
    line_chart.formatter=lambda x: '${:.2f}'.format(x)
    line_chart.y_title = 'Sales in $'
    line_chart.x_labels=['Qtr '+str(x) for x in range(1,5)]
    for x in dict:
        line_chart.add(str(x),dict[x])

    return line_chart

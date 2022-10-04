"""
Created on Mon June 6

@author: jairad26
"""

import json
import pygal
from pygal.style import Style
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

df = pd.read_csv("sales_data_sample.csv", encoding = 'unicode_escape')

custom_style = Style(
    plot_background = 'rgb(255,255,255,1)',
    background = 'transparent',

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


quarterly_revenue=df.groupby(['YEAR_ID','ORDERDATE'])['SALES'].sum().reset_index()
js = quarterly_revenue.to_json(orient='values')
data = json.loads(js)
dict=defaultdict(list)
dates_list = []
for x in data:
    if(x[0] == data[0][0]):
        dates_list.append(x[1])
    dict[x[0]].append(x[2])
    

lineChart = pygal.Line(dots_size=1, height=500, style=custom_style, value_formatter=lambda x: '${}'.format(x))
lineChart.title = 'Sales per Day'
# lineChart.x_labels = map(lambda d: d.strftime('%Y-%m-%d') )
lineChart.x_labels=[x for x in dates_list]
lineChart.formatter=lambda x: '${:.2f}'.format(x)

for x in dict:
    lineChart.add(str(x),dict[x])


lineChart.render_in_browser()


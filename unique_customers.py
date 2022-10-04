import json
import pygal
from pygal import style
from pygal.style import Style
import pandas as pd
from collections import defaultdict

df = pd.read_csv("sales_data_sample.csv", encoding = 'unicode_escape')

custom_style = Style(
    plot_background = 'rgb(255,255,255,1)',
    background = 'transparent',

    # Monospaced font is highly encouraged
    font_family = ('Sans Serif'),
    
    opacity = 0.8,
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
year_list=[]


for i in range(df["YEAR_ID"].size):
   if df["YEAR_ID"][i] not in year_list:
        year_list.append(df['YEAR_ID'][i])
    

#print(year_list)

df['CUSTOMER_FULL_NAME']=df['CONTACTFIRSTNAME'] + " " + df['CONTACTLASTNAME']
print(df['CUSTOMER_FULL_NAME'].head())





bar_chart=pygal.Bar(style=custom_style)
#bar_chart.x_labels = map(str, year_list)
bar_chart.title='# of Customers per year'

for i in year_list:
    unique_customers=0
    for j in range(df['ORDERNUMBER'].size):
        if df['YEAR_ID'][j] == i:
            unique_customers +=1
    bar_chart.add(str(i), unique_customers)  

#print(number_of_unique_customers)   
bar_chart.render_in_browser()














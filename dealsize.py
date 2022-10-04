import json
import pygal
from pygal.style import Style
import pandas as pd
from collections import defaultdict
from datetime import datetime
from csv import reader
import numpy as np

df = pd.read_csv("sales_data_sample.csv", encoding = 'unicode_escape')

custom_style = Style(
    plot_background = 'rgb(255,255,255,1)',
    background = 'transparent',

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

sales_low=df["SALES"][0]
sales_high=df["SALES"][0]


for i in range(df["SALES"].size):
    if df["SALES"][i] > sales_high:
        sales_high=df["SALES"][i]

for i in range(df["SALES"].size):
    if df["SALES"][i] < sales_low:
        sales_low=df["SALES"][i]

sales_range=(sales_high-sales_low)/5

first_quintile_sales=(sales_low + sales_range)
second_quintile_sales= (first_quintile_sales + sales_range)
third_quintile_sales= (second_quintile_sales + sales_range)
fourth_quintile_sales=(third_quintile_sales + sales_range)
fifth_quintile_sales=(fourth_quintile_sales + sales_range)

#print(first_tertile_sales)
#print(second_tertile_sales)
#print(third_tertile_sales)

def conditions(s):
    if(s["SALES"] <= first_quintile_sales):
        return "1st Quintile"
    elif(s["SALES"] <= second_quintile_sales):
        return "2nd Quintile"
    elif(s["SALES"] <= third_quintile_sales):
        return "3rd Quintile"
    elif(s["SALES"] <= fourth_quintile_sales):
        return "4th Quintile"
    else:
        return "5th Quintile"

df["SALES_SIZE"]=df.apply(conditions, axis=1)

#print(df.head())

number_of_1stQuintile_sales=0
number_of_2ndQuintile_sales=0
number_of_3rdQuintile_sales=0
number_of_4thQuintile_sales=0
number_of_5thQuintile_sales=0

for i in range(df["SALES_SIZE"].size):
    if df["SALES_SIZE"][i] == "1st Quintile":
        number_of_1stQuintile_sales+=1
    elif df["SALES_SIZE"][i]=="2nd Quintile":
        number_of_2ndQuintile_sales+=1
    elif df["SALES_SIZE"][i]=="3rd Quintile":
        number_of_3rdQuintile_sales+=1
    elif df["SALES_SIZE"][i]=="4th Quintile":
        number_of_4thQuintile_sales+=1
    elif df["SALES_SIZE"][i]=="5th Quintile":
        number_of_5thQuintile_sales+=1

quintile_sales=[]
quintile_sales.append(first_quintile_sales)
quintile_sales.append(second_quintile_sales)
quintile_sales.append(third_quintile_sales)
quintile_sales.append(fourth_quintile_sales)
quintile_sales.append(fifth_quintile_sales)


    
bar_chart=pygal.Bar()

bar_chart.add("$0" + " - " + str("${:.2f}".format(first_quintile_sales)), number_of_1stQuintile_sales)
bar_chart.add(str("${:.2f}".format(first_quintile_sales)) + "-" + str("${:.2f}".format(second_quintile_sales)), number_of_2ndQuintile_sales)
bar_chart.add(str("${:.2f}".format(second_quintile_sales)) + "-" + str("${:.2f}".format(third_quintile_sales)), number_of_3rdQuintile_sales)
bar_chart.add(str("${:.2f}".format(third_quintile_sales)) + "-" + str("${:.2f}".format(fourth_quintile_sales)), number_of_4thQuintile_sales)
bar_chart.add(str("${:.2f}".format(fourth_quintile_sales)) + "-" + str("${:.2f}".format(fifth_quintile_sales)), number_of_5thQuintile_sales)


bar_chart.render_in_browser()



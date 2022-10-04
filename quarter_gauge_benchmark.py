import json
import pygal
from pygal.style import Style
import pandas as pd

def quarter_gauge_benchmark():
    df = pd.read_csv("sales_data_sample.csv", encoding = 'unicode_escape')


    custom_style = Style(
        plot_background = 'rgb(255,255,255,1)',
        background = 'rgb(255,255,255,1)',

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





    quarterly_revenue=df.groupby(['YEAR_ID','QTR_ID'])['SALES'].sum().reset_index()
    js = quarterly_revenue.to_json(orient='values')
    data = json.loads(js)
    print(data)

    expected_revenueQ1=int(input("Enter your expected revenue for Quarter 1 this year:"))
    expected_revenueQ2=int(input("Enter your expected revenue for Quarter 2 this year:"))
    expected_revenueQ3=int(input("Enter your expected revenue for Quarter 3 this year:"))
    expected_revenueQ4=int(input("Enter your expected revenue for Quarter 4 this year:"))


    qtr1_value=0
    qtr2_value=0
    qtr3_value=0
    qtr4_value=0

    for x in data:
        if x[0] == year_list[len(year_list)-1] and x[1] == 1:
            qtr1_value=x[2]

    for x in data:
        if x[0] == year_list[len(year_list)-1] and x[1] == 2:
            qtr2_value=x[2]

    for x in data:
        if x[0] == year_list[len(year_list)-1] and x[1] == 3:
            qtr3_value=x[2]

    for x in data:
        if x[0] == year_list[len(year_list)-1] and x[1] == 4:
            qtr4_value=x[2]



    gauge = pygal.SolidGauge(
        half_pie=True, inner_radius=0.70,
        style=custom_style)

    percent_formatter = lambda x: '{:.10g}%'.format(x)
    dollar_formatter = lambda x: '{:.10g}$'.format(x)
    gauge.value_formatter = percent_formatter






    gauge.add('Benchmark for Quarter 1 in $', [{'value': qtr1_value, 'max_value': expected_revenueQ1}], formatter=dollar_formatter)
    gauge.add('Benchmark for Quarter 2 in $', [{'value': qtr2_value, 'max_value': expected_revenueQ2}], formatter=dollar_formatter)
    gauge.add('Benchmark for Quarter 1 in $', [{'value': qtr3_value, 'max_value': expected_revenueQ3}], formatter=dollar_formatter)
    gauge.add('Benchmark for Quarter 1 in $', [{'value': qtr4_value, 'max_value': expected_revenueQ4}], formatter=dollar_formatter)
    gauge.render_in_browser()
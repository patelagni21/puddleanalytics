
import json
import pygal
from pygal.style import Style
import pandas as pd
from collections import defaultdict



def revenue_by_product_radar(filename):
    df = pd.read_csv(filename,sep=";", encoding = 'ISO-8859-1')

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

    productRevenue= df.groupby(['YEAR_ID','PRODUCTLINE'])['SALES'].sum().reset_index()
    productRevenuePerYear = productRevenue.groupby(['YEAR_ID'])['SALES'].sum().reset_index()
    yearRevDictIndex = productRevenuePerYear.to_dict(orient='index')
    yearRevDict = {}
    for x in yearRevDictIndex:
        yearRevDict[yearRevDictIndex[x]['YEAR_ID']] = yearRevDictIndex[x]['SALES']
    possibleProducts = productRevenue['PRODUCTLINE'].unique()
    js = productRevenue.to_json(orient='values')
    data = json.loads(js)
    
    dict=defaultdict(list)
    
    for x in data:
        dict[x[0]].append(x[2])


    radar_chart=pygal.Radar(style=custom_style)
    percent_formatter = lambda x: '{:.2f}%'.format(x)
    radar_chart.value_formatter = percent_formatter
    # radar_chart.title='Revenue of Different Products per Year (in %)'
    radar_chart.x_labels = possibleProducts
    for x in dict:
        radar_chart.add(str(x), [i/int(yearRevDict[x])*100 for i in dict[x]])

    return radar_chart
    # radar_chart.render_in_browser()
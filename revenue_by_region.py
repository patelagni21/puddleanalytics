import json
import pygal
from pygal.style import Style
import pandas as pd

def revenue_by_region(filename):
    df = pd.read_csv(filename, sep=";",encoding = 'ISO-8859-1')


    country_code=pd.read_csv("country_code.csv", encoding='mac-roman')
    country_code['Code']=country_code['Code'].str.lower()

    pd.options.mode.chained_assignment = None


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
        colors = ( '#0f6987', '#bc5190', '#ffa600', '#3b4d80', '#E89B53'))


    for i in range(df['COUNTRY'].size):
        for x in range(country_code['Name'].size):
            if df['COUNTRY'][i]==country_code['Name'][x]:
                df['COUNTRY'][i]=country_code['Code'][x]





    region_revenue=df.groupby(['COUNTRY'])['SALES'].sum().reset_index()
    js = region_revenue.to_json(orient='records')
    data = json.loads(js)

    dict = {}
    for i in data:
        dict[i['COUNTRY']] = i['SALES']


    revenue_map=pygal.maps.world.World(style=custom_style, value_formatter=lambda x: '${:.2f}'.format(x))
    # revenue_map.title= "Total Revenue by Region"

    revenue_map.add('Revenue in $', dict)

    return revenue_map
import imp
from turtle import color, width
import dash
import dash_core_components as dcc
import dash_html_components as html
from matplotlib.pyplot import autoscale, figure, legend
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = dash.Dash()

df = pd.read_excel(
    "All_data.xlsx"
)
continent_df = pd.read_excel(
    'Continent_data.xlsx'
)

app.layout = html.Div([
    html.H1('Human Metrics', style={'height':'4vh'}),
    html.Div([
        html.H2( id='choices') ,
        dcc.Dropdown(df['Country'].unique(),placeholder='Select Country', multi=True, id='Country-Select'),
        dcc.Graph(id="suicide-vs-hdi", style={'height':'80vh'})],
        style={'height': 0,'width':'59vw','font_size':75, 'display' : 'inline-block'}, className='abc'),
        #/div
    html.Div([
        dcc.Dropdown(['HDI', 'GDI', 'Suicide Rate', 'Male Suicide Rate', 'Female Suicide Rate', 'Life Expectancy'], placeholder='X Attribute',id='x-select'),
        dcc.Dropdown(['HDI', 'GDI', 'Suicide Rate', 'Male Suicide Rate', 'Female Suicide Rate', 'Life Expectancy'], placeholder='Y Attribute',id='y-select'),
        dcc.Graph(id='line-plot1', style={'height':'40vh'}),
        dcc.Graph(id='line-plot2', style={'height':'40vh'})],
        style={'height': 0,'width':'39vw','font_size': 75, 'display' : 'inline-block'}, className='abc'),
    ])

@app.callback(
    Output('suicide-vs-hdi', 'figure'),
    Output('line-plot1', 'figure'),
    Output('line-plot2', 'figure'),
    Output('choices', 'children'),
    Input('Country-Select', 'value'),
    Input('x-select', 'value'),
    Input('y-select', 'value')
)

def update_figure(countries, x_val, y_val):
    print(countries, x_val, y_val)
    x_axis = 'HDI'
    y_axis = 'Suicide Rate'
    if countries == None or countries == [] or countries == 'Select Country':
        new_df=df
        line_df = continent_df
        line_hover = 'Region'
    else:
        new_df = df[df['Country'].isin(countries)]
        line_df = df[df['Country'].isin(countries)]
        line_hover = 'Country'
    if x_val != None and x_val != '':
        x_axis = x_val
    if y_val != None and y_val != '':
        y_axis = y_val
    fig = px.line(
        line_df,
        x = 'Year',
        y = x_axis,
        color=line_hover,
        hover_name=line_hover,
    )
    fig.update_layout(showlegend = False)
    fig1 = px.line(
        line_df,
        x = 'Year',
        y = y_axis,
        color=line_hover,
        hover_name=line_hover
    )
    fig1.update_layout(showlegend = False)
    fig2 = px.scatter(
        new_df,
        x = x_axis,
        y = y_axis,
        color=line_hover,
        animation_frame = "Year",
        hover_name="Country",
        range_x = (0, new_df[x_axis].max()),
        range_y = (0, new_df[y_axis].max()),
        labels={
            line_hover : '<b>' + line_hover + '</b>',
            y_axis : '<b>' + y_axis + '</b>',
            x_axis: '<b>' + x_axis + '</b>'
        }
    )
    fig2.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ))

    return fig2, fig, fig1, x_axis + " Vs. " + y_axis 

if __name__ == "__main__":
    app.run_server(debug=True)
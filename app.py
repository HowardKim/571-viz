import dash
import dash_core_components as dcc
import dash_html_components as html
from matplotlib.pyplot import figure
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash()

df = pd.read_excel(
    "All_data.xlsx"
)

fig = px.scatter(
    df,
    x="HDI",
    y="Suicide Rate",
    color="ParentLocation",
    animation_frame = "Year",
    hover_name="Country",
    range_x=[0.2,1],
    range_y=[0,75]
)

app.layout = html.Div([
    html.H1("Suicide Rate vs Human Development"),
    html.Div([
        html.H2('Select Country'),
        dcc.Dropdown(df['Country'].unique(), multi=True, id='Country-Select'),
    ]),
    dcc.Graph(id="suicide-vs-hdi", figure=fig, style={'height':'80vh', 'width':'60vw'})])

@app.callback(
    Output('suicide-vs-hdi', 'figure'),
    Input('Country-Select', 'value')
)

def update_figure(countries):
    print(countries)
    if countries == None or countries == []:
        return fig
    new_df = df[df['Country'].isin(countries)]
    fig2 = px.scatter(
        new_df,
        x="HDI",
        y="Suicide Rate",
        color="ParentLocation",
        animation_frame = "Year",
        hover_name="Country",
        range_x=[0.2,1],
        range_y=[0,75]
    )
    return fig2

if __name__ == "__main__":
    app.run_server(debug=True)
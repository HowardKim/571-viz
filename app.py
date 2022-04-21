import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

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


if __name__ == "__main__":
    app.run_server(debug=True)
import os
from pandas.core.frame import DataFrame
from pyairtable import Table
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
api_key = 'keyrS9j6UtUM8dpmM'
raw_data = []

table = Table(api_key, 'appn70zbAeXjt7tcC', 'Organizations')
list = table.all()

for record in list:
    d = record['fields']
    raw_data.append(d)

df = DataFrame(raw_data)

total = len(df.index)
type = px.histogram(df, x="Stakeholder Type", histnorm='percent')
year = px.histogram(df, x="Year Founded", histnorm='percent')
state = px.histogram(df, x="Headquarters (State)", histnorm='percent')
city = px.histogram(df, x="Headquarters (City)", histnorm='percent')
programs = px.histogram(df, x="Programs (Activities)") # Needs to be unnested
customers = px.histogram(df, x="Primary Customer") # Needs to be unnested
reach = px.histogram(df, x="Reach", histnorm='percent')
focus = px.histogram(df, x="Race/Ethnic Focus", histnorm='percent')

app.layout = html.Div([
    html.H1('BIA Dashboard'),
    dcc.Tabs(id="tabs-data", value='type', children=[
        dcc.Tab(label='Stakeholder Type', value='type'),
        dcc.Tab(label='Year Founded', value='year'),
        dcc.Tab(label='State', value='state'),
        dcc.Tab(label='City', value='city'),
        dcc.Tab(label='Programs', value='programs'),
        dcc.Tab(label='Customers', value='customers'),
        dcc.Tab(label='Reach', value='reach'),
        dcc.Tab(label='Focus', value='focus'),
    ]),
    html.Div(id='dashboard', children="A dashboard with up to date stats on original Black CensUs Survey")
])

@app.callback(Output('dashboard', 'children'),
              Input('tabs-data', 'value'))
def render_content(tab):
    if tab == 'type':
        return html.Div([
            html.H3('Stakeholder Type'),
            dcc.Graph(
                id='type-graph',
                figure=type
            )
        ])
    elif tab == 'year':
        return html.Div([
            html.H3('Year Founded'),
            dcc.Graph(
                id='year-graph',
                figure=year
            )
        ])
    elif tab == 'state':
        return html.Div([
            html.H3('States'),
            dcc.Graph(
                id='state-graph',
                figure=state
            )
        ])
    elif tab == 'city':
        return html.Div([
            html.H3('City'),
            dcc.Graph(
                id='city-graph',
                figure=city
            )
        ])
    # elif tab == 'programs':
    #     return html.Div([
    #         html.H3('Programs'),
    #         dcc.Graph(
    #             id='programs-graph',
    #             figure=programs
    #         )
    #     ])
    # elif tab == 'customers':
    #     return html.Div([
    #         html.H3('Customers'),
    #         dcc.Graph(
    #             id='customers-graph',
    #             figure=customers
    #         )
    #     ])
    elif tab == 'reach':
        return html.Div([
            html.H3('Reach'),
            dcc.Graph(
                id='reach-graph',
                figure=reach
            )
        ])
    elif tab == 'focus':
        return html.Div([
            html.H3('Race/Ethnicity Focus'),
            dcc.Graph(
                id='focus-graph',
                figure=focus
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
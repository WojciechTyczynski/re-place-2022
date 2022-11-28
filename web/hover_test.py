import json
from textwrap import dedent as d
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
# app info
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# data and basic figure
x = np.arange(20)+10

fig = go.Figure(data=go.Scatter(x=x, y=x**2, mode = 'lines+markers'))
fig.add_traces(go.Scatter(x=x, y=x**2.2, mode = 'lines+markers'))

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig,
    ),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown(d("""
              Click on points in the graph.
            """)),
            html.Pre(id='hover-data', style=styles['pre']),
        ], className='three columns'),
    ])
])


@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

app.run_server(mode='external', port = 8070, dev_tools_ui=True,
          dev_tools_hot_reload =True, threaded=True)
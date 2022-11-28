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


action_per_user = pd.read_csv('./assets/interactions_pr_user.csv')

# app info
app = dash.Dash()

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# data and basic figure
y = np.arange(100)+10
x = pd.date_range(start='1/1/2021', periods=len(y))

fig = go.Figure(data=go.Scatter(x=x, y=y**2, mode = 'lines+markers'))
fig.add_traces(go.Scatter(x=x, y=y**2.2, mode = 'lines+markers'))

app.layout = html.Div([
    dcc.Graph(
            id='interaction-per-user-graph-2',
            config={'doubleClick': 'reset'},
            figure={
                'data': [
                    {'x': action_per_user['user_id'], 'y': action_per_user['count'], 'type': 'bar', 'name': 'SF'},
                ],
                'layout': {
                    'title': 'Interactions per user'
                }
            },
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
    try:
        return json.dumps({'Date:':hoverData['points'][0]['x'],
                           'Value:':hoverData['points'][0]['y']}, indent = 2)
    except:
        return None

app.run_server(debug=True)
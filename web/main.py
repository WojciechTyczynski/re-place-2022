import imp
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
import dash_daq as daq
import plotly.express as px

import plotly.graph_objects as go

import pandas as pd
import numpy as np
import json

import os

# import Image
from PIL import Image
#  set working directory
os.chdir(os.getcwd())
# Opening JSON file
with open('./assets/dict_hours_images.json') as json_file:
    dict_hours_images = json.load(json_file)

atlas_df = pd.read_json('./assets/atlas_small.json')
 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

action_per_hour = pd.read_csv('./assets/interactions_pr_hour.csv')

# app = Dash(__name__, external_stylesheets=external_stylesheets)
app = DashProxy(transforms=[MultiplexerTransform()], external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
        dcc.Tab(label='r/place - communities and atlas', value='tab-1', children=[
            html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(""), width="auto"),
                        dbc.Col(
                            html.Div([
                                html.H3('The 2022 r/place timeline and atlas'),
                                html.Div([
                                dcc.Graph(
                                    id='image-with-slider',
                                    config={'doubleClick': 'reset'},
                                    ),
                                ]),
                            html.Div([
                                daq.Slider(
                                    min=0,
                                    max=81,
                                    step=1,
                                    value=81,
                                    size=1000,
                                    id='hour-slider',
                                    handleLabel={"showCurrentValue": True,"label": "Hours"},)
                                    ], style={}),
                            html.Div([
                                dcc.Checklist(
                                    id='checklist',
                                    options=[
                                        {'label': 'Show Atlas Layer', 'value': 'show_atlas'},
                                    ],
                                    value=['show_atlas']
                                    ),
                                ]),
                        ], style={'align-items': 'center', 'justify-content': 'center', 'display': 'inline-block', 'margin-left': 'auto', 'width': '100%'}),
                        width="auto"),
                        dbc.Col(
                            html.Div(children=[
                                dcc.Markdown(
                                    '''
                                    ### r/place timeline
                                    This is some test to see if this works
                                    '''
                                ),
                                html.H3(id='atlas-name'),
                                # html.Pre(id='hover-data', style=styles['pre']),
                                dcc.Markdown(id='atlas_description'),
                    ]),
                            width="3"
                            ),
                    ]),
            ]),
    ]),
        dcc.Tab(label='r/place analysis', value='tab-2', children=[
            html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='interaction-per-h-graph-2',
                config={'doubleClick': 'reset'},
                figure={
                    'data': [
                        {'x': action_per_hour['timestamp'], 'y': action_per_hour['count'], 'type': 'bar', 'name': 'SF'},
                    ],
                    'layout': {
                        'title': 'Interactions per hour'
                    }
                },
            )
        ], style={'margin': '0 auto','align-items': 'center'}),
            html.Div(children = [
                html.Iframe(
                    # controls = True,
                    id = 'movie_player',
                    src = "https://www.youtube.com/embed/lKWqIg4nZKs",
                    width = "1000px",
                    # autoPlay=True,
                    # loop=True,
                    style={"height": "720px", "width": "720px", 'margin-left': '25 auto'},),
        ])
        ]
            ),
    ]),
    html.Div(id='tabs-example-content-1'),    
], style={'align-items': 'center', 'justify-content': 'center', 'display': 'inline-block', 'margin': '25 auto', 'width': '100%'})




@app.callback(
    Output('image-with-slider', 'figure'),
    Input('hour-slider', 'value'),
    Input('checklist', 'value'))
def update_figure(selected_hour, checklist):
    # Create figure
    fig = go.Figure()

    # Constants
    img_width = 1000
    img_height = 1000
    scale_factor = 1
    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.

    # Scaled atlas shapes    
    atlas_df['x_scaled']  = atlas_df['x'].apply(lambda x: np.array(x) * scale_factor)
    atlas_df['y_scaled']  = atlas_df['y'].apply(lambda x: np.array(x) * scale_factor)
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )
    
    if 'show_atlas' in checklist:
        for i in range(len(atlas_df)):
            fig.add_trace(
                go.Scatter(
                    x=atlas_df.x_scaled.loc[i],
                    y=atlas_df.y_scaled.loc[i],
                    mode='lines',
                    fill="toself",
                    # hoveron='points+fills',
                    # customdata=[atlas_df.name.loc[i], atlas_df.description.loc[i]],
                    # hovertext=atlas_df.name.loc[i],
                    # text=atlas_df.name.loc[i]
                    name=atlas_df.name.loc[i],
                )
            )


    image_path = dict_hours_images[str(selected_hour)]
    print(image_path)

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=(img_height * scale_factor) - (img_height * scale_factor),
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source=image_path)
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor],
        constrain="domain"
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x",
        autorange="reversed",
        constrain="domain"
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        showlegend=False
    )

    # Disable the autosize on double click because it adds unwanted margins around the image
    # More detail: https://plotly.com/python/configuration-options/
    # fig.show(config={'doubleClick': 'reset'})
    return fig

@app.callback(
    Output('atlas_description', 'children'),
    Output('atlas-name', 'children'),
    [Input('image-with-slider', 'hoverData'),
    Input('checklist', 'value')])
def display_hover_data(hoverData, checklist):
    if 'show_atlas' in checklist:
        try:
            id  = hoverData['points'][0]['curveNumber'] - 1
            hoverData['points'][0]['name'] = atlas_df.name.loc[id]
            hoverData['points'][0]['description'] = atlas_df.description.loc[id]
            # return json.dumps(hoverData, indent=2)
            figure_name = hoverData['points'][0]['name']
            figure_description = f'''
            {hoverData['points'][0]['description']}
            '''
            return figure_description, figure_name
        except:
            # return json.dumps(hoverData, indent=2)
            return None, None
    else:
        return None, None
    

if __name__ == '__main__':
    app.run_server(debug=True)

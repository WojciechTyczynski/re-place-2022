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

with open('./assets/dict_raw_images.json') as json_file:
    dict_raw_images = json.load(json_file)
    
with open('./assets/dict_communities_denoised.json') as json_file:
    dict_communities_denoised = json.load(json_file)

with open('./assets/dict_communities_raw.json') as json_file:
    dict_communities_raw = json.load(json_file)

atlas_df = pd.read_json('./assets/atlas_small.json')
atlas_400_df = pd.read_json('./assets/atlas_small_400.json')
 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

action_per_hour = pd.read_csv('./assets/interactions_pr_hour.csv')
action_per_pixel = pd.read_csv('./assets/interactions_pr_pixel.csv')
action_per_user = pd.read_csv('./assets/interactions_pr_user.csv')
action_per_pixel = action_per_pixel[(action_per_pixel['x1'] <  1000) & (action_per_pixel['y1'] < 1000)]

viridis = px.colors.sequential.Viridis
colorscale = [
        [0, viridis[0]],
        [1./1000000, viridis[2]],
        [1./10000, viridis[4]],
        [1./100, viridis[7]],
        [1., viridis[9]],
    ]
colorbar= dict(
        tick0= 0,
        tickmode= 'array',
        tickvals= [0, 1000, 10000]
    )

#Figures
fig_action_per_user  = go.Figure(data=go.Histogram(histfunc="count", x=action_per_user['count'], nbinsx=100))
fig_action_per_user.update_yaxes(type='log')
fig_action_per_user.update_layout(template='plotly_white', title_x=0.5, title_text='Number of interactions per user')

fig_action_per_pixel  = go.Figure(data=go.Heatmap(
                   z=action_per_pixel['count'],
                   x=action_per_pixel['x1'],
                   y=action_per_pixel['y1'],
                   colorscale=colorscale,))

fig_action_per_pixel.update_layout(
        template='plotly_white',
        title_x=0.5,
        width=1000,
        height=1000,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        showlegend=False,
    )

fig_action_per_pixel.update_xaxes(visible=False, showticklabels=False)
fig_action_per_pixel.update_yaxes(scaleanchor = "x", autorange="reversed", visible=False, showticklabels=False)

# app = Dash(__name__, external_stylesheets=external_stylesheets)
app = DashProxy(transforms=[MultiplexerTransform()], external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
        dcc.Tab(label='r/place - Intro', value='tab-1',children=[
            html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(""), width="auto"),
                        dbc.Col(
                            html.Div([
                                html.H2('The 2022 r/place timeline and atlas'),
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
                                    value=['show_atlas'],
                                    labelStyle = {'display':'block', 'font-size': 16, 'color': 'black', 'margin-left': '10px', 'margin-right': 'auto', 'width': '100%', 'text-align': 'left'},
                                    ),
                                ]),
                        ], style={'align-items': 'center', 'justify-content': 'center', 'display': 'inline-block', 'margin-left': 'auto', 'width': '100%'}),
                        width="auto"),
                        dbc.Col(
                            html.Div(children=[
                                dcc.Markdown(
                                    '''
                                    ## Project description
                                    This web application shows you the timeline of Reddit r/place from April 2022 and the overlay from Reddit [r/place atlas]  (https://place-atlas.stefanocoding.me/)  created by Roland Rytz. It is capped to 1000x1000px, and aims to show another way of capturing communities than the manual process that Roland Rytz started. By analyzing all the entries on r/place and creating a graph of all the interactions, we have discovered communities and found their outlines only by looking at how people interact. 
                                    The graph is modelled by creating a node for each color for each pixel, meaning that we get 16 different nodes for each pixel. Then we make an edge to one of these nodes from a user if a user has used that color-pixel. When we have this graph, then we can do community detection on the graph, and see where the different communities place their pixels. 
                                    ''',
                                    style={'font-size': 14, 'color': 'black', 'margin-left': '10px', 'margin-right': 'auto', 'width': '100%', 'text-align': 'left'},
                                ),
                                html.H3(id='atlas-name'),
                                # html.Pre(id='hover-data', style=styles['pre']),
                                dcc.Markdown(id='atlas_description', style={'font-size': 14, 'color': 'black', 'margin-left': '10px', 'margin-right': 'auto', 'width': '100%', 'text-align': 'left'}),
                    ]),
                            width="3"
                            ),
                    ]),
            ]),
    ]),
        dcc.Tab(label='r/place analysis', value='tab-2', children=[
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div(
                        dcc.Graph(
                            id='interaction-per-h-graph-2',
                            config={'doubleClick': 'reset'},
                            figure={
                                'data': [
                                    {'x': action_per_hour['timestamp'], 'y': action_per_hour['count'], 'type': 'bar', 'name': 'SF'},
                                ],
                                'layout': {
                                    'title': 'Interactions per hour',
                                    'template': 'plotly_white'
                                }
                            },
                        ),
                ),),
            ]),
            dbc.Row([
                    dbc.Col(html.Div(
                        dcc.Graph(
                            id='interaction-per-user-graph-2',
                            config={'doubleClick': 'reset'},
                            figure=fig_action_per_user,
                        ),
                ),),
            ]),
            html.H2('Interactions per pixel'),
            dbc.Row([
                    dbc.Col(html.Div()),
                    dbc.Col(html.Div(children = [
                        html.Iframe(
                            # controls = True,
                            id = 'movie_player',
                            src = "https://www.youtube.com/embed/lKWqIg4nZKs",
                            width = "2000px",
                            # autoPlay=True,
                            # loop=True,
                            style={"height": "1000px", "width": "1000px", 'margin-left': '25 auto'},),
                            ])),
                    dbc.Col(html.Div()),
                    dbc.Col(html.Div(children = [
                        dcc.Graph(
                                id='interaction-per-pixel-graph-2',
                                config={'doubleClick': 'reset'},
                                figure=fig_action_per_pixel,
                                ),
                            ])),
                    dbc.Col(html.Div()),
            ]),
        ], style={'margin': '0 auto','align-items': 'center'}),
        ]
            ),
        dcc.Tab(label='r/place atlas & communities', value='tab-3', children=[
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div(""), width="auto"),
                        dbc.Col(
                            html.Div([
                                html.H3('The 2022 r/place timeline and atlas'),
                                html.Div([
                                dcc.Graph(
                                    id='image-with-slider-2',
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
                                    id='hour-slider-2',
                                    handleLabel={"showCurrentValue": True,"label": "Hours"},)
                                    ], style={}),
                            html.Div([
                                dcc.Checklist(
                                    id='checklist-2',
                                    options=[
                                        {
                                            'label': 'Show picture', 
                                            'value': 'show_picture'
                                        },
                                        {
                                            'label': 'Show Atlas Layer',
                                            'value': 'show_atlas',
                                        },
                                        {
                                            'label': 'Show communities', 
                                            'value': 'show_communities'
                                        },
                                        {
                                            'label': 'Show communities - denoised', 
                                            'value': 'show_communities_denoised'
                                        },

                                    ],
                                    value=['show_picture'],
                                    labelStyle = {'display':'block', 'font-size': 16, 'color': 'black', 'margin-left': '10px', 'margin-right': 'auto', 'width': '100%', 'text-align': 'left'},
                                    ),
                                ], style={'display': 'block', 'margin-left': 'auto', 'width': '100%'}),
                        ], style={'align-items': 'center', 'justify-content': 'center', 'display': 'block' ,'margin-left': 'auto', 'width': '100%'}),
                        width="auto"),
                ]),
            ]),
        ]),
    ]),
    html.Div(id='tabs-example-content-1'),    
], style={'align-items': 'center', 'justify-content': 'center', 'display': 'block', 'margin': '25 auto', 'width': '100%'})




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
                go.Scattergl(
                    x=atlas_df.x_scaled.loc[i],
                    y=atlas_df.y_scaled.loc[i],
                    mode='lines',
                    fill="toself",
                    opacity=0.5,
                    # hoveron='points+fills',
                    # customdata=[atlas_df.name.loc[i], atlas_df.description.loc[i]],
                    hovertext=atlas_df.name.loc[i],
                    # text=atlas_df.name.loc[i],
                    name=atlas_df.name.loc[i]
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
    

@app.callback(
    Output('image-with-slider-2', 'figure'),
    Input('hour-slider-2', 'value'),
    Input('checklist-2', 'value'))
def update_figure_2(selected_hour, checklist):
    # Create figure
    fig = go.Figure()

    # Constants
    original_img_width = 400
    original_img_height = 400
    img_width = 1000
    img_height = 1000
    scale_factor = 1
    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.

    # Scaled atlas shapes    
    atlas_400_df['x_scaled']  = atlas_400_df['x_cropped'].apply(lambda x: np.array(x) * (img_width/original_img_width) * scale_factor)
    atlas_400_df['y_scaled']  = atlas_400_df['y_cropped'].apply(lambda x: np.array(x) * (img_height/original_img_height) * scale_factor)
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )
    
    if 'show_atlas' in checklist:
        for i in range(len(atlas_400_df)):
            fig.add_trace(
                go.Scatter(
                    x=atlas_400_df.x_scaled.loc[i],
                    y=atlas_400_df.y_scaled.loc[i],
                    mode='lines',
                    line=dict(color='black', width=3),
                    fill="toself",
                    fillcolor='rgba(0,0,0,0.05)',
                    opacity=1,
                    hoveron='points+fills',
                    # customdata=[atlas_df.name.loc[i], atlas_df.description.loc[i]],
                    hovertext=atlas_400_df.name.loc[i],
                    # text=atlas_df.name.loc[i],
                    name=atlas_400_df.name.loc[i]
                )
            )


    image_path = dict_raw_images[str(selected_hour)]
    comunity_raw_image = dict_communities_raw[str(selected_hour)]
    comunity_raw_denoised = dict_communities_denoised[str(selected_hour)]
    print(image_path)

    # Add image
    if 'show_picture' in checklist:
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
    
    # Add comunity raw image
    if 'show_communities' in checklist:
        fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=(img_height * scale_factor) - (img_height * scale_factor),
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                opacity=0.75,
                layer="below",
                sizing="stretch",
                source=comunity_raw_image)
        )

    # Add comunity denoised image
    if 'show_communities_denoised' in checklist:
        fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=(img_height * scale_factor) - (img_height * scale_factor),
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                opacity=0.85,
                layer="below",
                sizing="stretch",
                source=comunity_raw_denoised)
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


if __name__ == '__main__':
    app.run_server(debug=True)


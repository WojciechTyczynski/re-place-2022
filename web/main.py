import imp
from dash import Dash, dcc, html, Input, Output
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
with open('dict_hours_images.json') as json_file:
    dict_hours_images = json.load(json_file)
 

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='image-with-slider'),
    dcc.Slider(
        0,
        72,
        step=1,
        value=0,
        id='hour-slider', 
        tooltip={"placement": "bottom", "always_visible": True}
    )
])


@app.callback(
    Output('image-with-slider', 'figure'),
    Input('hour-slider', 'value'))
def update_figure(selected_hour):
    # Create figure
    fig = go.Figure()

    # Constants
    img_width = 1000
    img_height = 1000
    scale_factor = 0.5

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    image_path = dict_hours_images[str(selected_hour)]
    print(image_path)

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source=image_path)
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    # Disable the autosize on double click because it adds unwanted margins around the image
    # More detail: https://plotly.com/python/configuration-options/
    # fig.show(config={'doubleClick': 'reset'})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

import pandas as pd
from graph_tool.all import *
import numpy as np
import matplotlib
import csv
from datetime import datetime
import fastparquet
from tqdm import tqdm

from PIL import Image
import os
class PlaceCanvas:
    def __init__(self, width, height):
        self.canvas = Image.new('RGB', (width, height), color = 'white')


    def update_pixel(self, x,y,color):
        """
        Sets the specific x,y coordinate in the canvas to the given hex color.

        example:
        update_pixel(10,10,"#B4FBB8")
        """
#         h = color.lstrip('#')
#         rgb_value = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
#         self.canvas.putpixel((x,y), rgb_value)
        self.canvas.putpixel((x,y), color)

    def save_canvas(self, path = "images/"):
        if(os.path.exists(f'{path}images.png')):
            i = 0 
            while(os.path.exists(f'{path}images {i}.png')):
                i += 1
            self.canvas.save(f'{path}images {i}.png')
        else:
            self.canvas.save(f'{path}images.png')

    def get_image(self):
        return self.canvas
		
v_con_sub_g = Graph(directed = False)
v_con_sub_g.load('graph_filtered.gt')

state = minimize_blockmodel_dl(v_con_sub_g)
b = state.get_blocks()

df = pd.DataFrame(np.column_stack([list(sub_g.vp.v_id), list(b.a),list(sub_g.vp.v_type)]), columns=['id','community','type'])
df_last = pd.DataFrame(np.column_stack([list(sub_g.vp.v_id), list(sub_g.vp.v_last_action_user),list(sub_g.vp.v_type)]), columns=['id','last', 'type'])
df_last['pixel'] = df_last[df_last.type=="1"].id.str.split('|')

last_pixel = pd.DataFrame(np.column_stack([list(dict_pixel.keys()), list(dict_pixel.values())]), columns = ['coords','user'])
user_community = df[(df.community != 0) & (df.type == '0')]

df_vis = pd.merge(last_pixel, user_community, how = 'left', left_on='user', right_on = 'id')
df_vis = df_vis.dropna()[['coords','community']]
df_vis.to_csv('df_vis.csv')
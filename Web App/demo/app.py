import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import os
import numpy as np
import logging
from PIL import Image
import base64
import io
import plotly.graph_objs as go
import pickle
import cv2

from dash.dependencies import Input, Output, State
from IPython.display import display, IFrame, HTML

from dash.exceptions import PreventUpdate
import json
import os
import time
import uuid
from copy import deepcopy
import csv
import sys
import pathlib
import importlib
from flask_caching import Cache
import dash_reusable_components as drc
import utils as utils

import keras
from keras.models import load_model

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
# external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/cerulean/bootstrap.min.css']


APP_PATH = str(pathlib.Path(__file__).parent.resolve())
DEBUG = True
LOCAL = True

app = dash.Dash(__name__,  external_stylesheets=external_stylesheets)
server = app.server

product_df = pd.read_csv('data/products.csv')
labels = product_df['Products'].unique()
labels_values = product_df['Links'].unique()
options = [{'label': x, 'value': y} for x,y in zip(labels,labels_values)]

#Scaling within range 1-10
def scaling(x,a,b,minimum,maximum):
    return float(((b-a)*(x-minimum)/(maximum-minimum))+a)

# resets the callbacks
app.callback_map = {}

# sets the title
app.title = 'Ecfullfill Capstone'

# html content
app.layout = html.Div([

                #Card Groups
            html.Div([
                html.Div([
                    html.Div(id='output-container-button-5',
                             children='Enter Price'),
                    html.Div(dcc.Input(id='input-box-5', type='text',required=True,
                        style={'position':'relative'})),
                    html.Button('Submit', id='button-5',
                        style={'position':'relative'}),
                ],className='two columns'),

            ],className='row'),

            html.Br(),
            html.Br(),

            #Select Products
            html.Div([
                html.Div([
                    html.Div(id='output-container-button-6',
                             children='Select Product'),
                    dcc.Dropdown(
                        id='product-dropdown',
                        options=options,value='shampoo'),
                ],className='six columns'),

                html.Div([
                    html.Div(id='output-container-button-7',
                             children='Select Tags'),
                    dcc.Dropdown(
                        id='multi-dropdown',
                        multi=True),
                    html.Div(id='display-selected-values'),
                ],className='six columns')
            ],className='row'),

        html.Br(),
        html.Br(),

    html.Div([
        dcc.Tabs([
            # Tab 1
            dcc.Tab([
                    html.Div([
                        dcc.Upload(
                            id='upload-image',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Image')
                            ]),
                            style={
                                'width': '90%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            accept="image/*",

                            # Dont Allow multiple files to be uploaded
                            multiple=True
                        ),

                        html.Div([
                            #Product Length Button
                            html.Div([
                                html.Div(dcc.Input(id='product-length', type='text',required=True, placeholder = 'Product Length (in)',
                                    style={'position':'relative'})),
                            ],className = 'two columns'),
                            #Product Width Button
                            html.Div([
                                html.Div(dcc.Input(id='product-width', type='text',required=True, placeholder = 'Product Width (in)',
                                    style={'position':'relative'})),
                            ],className = 'two columns'),
                            #Product Height Button
                            html.Div([
                                html.Div(dcc.Input(id='product-height', type='text',required=True, placeholder = 'Product Height (in)',
                                    style={'position':'relative'})),
                            ],className = 'two columns'),
                            #Product Weight Button
                            html.Div([
                                html.Div(dcc.Input(id='product-weight', type='text',required=True, placeholder = 'Product Weight (oz)',
                                    style={'position':'relative'})),
                            ],className = 'two columns'),
                            html.Div([
                                html.Button(id='run-operation', n_clicks=0, children='Run Operation'),
                                html.Div(id='run-model'),
                            ],className = 'two columns'),
                        ], className = 'row'),
                    ],className='row'),

                    html.Br(),
                    html.Br(),

                    html.Div([
                        #Upload COmponent
                        html.Div([
                            #Image Upload Graph
                            html.Div([
                                dcc.Graph(id='image_graph')
                            ])
                        ],className='six columns'),

                        #World Map
                        html.Div([
                            html.Div([
                                    dcc.Graph(id='the_graph')
                                ]),
                            html.Div([
                                html.Div(id='output_state'),
                            ]),
                        ],className='six columns')
                    ],className = 'row'),
                ], className="container-fluid", label="Product Perfomance Insight"),



            # Tab 2
            dcc.Tab([
                    dcc.Textarea(
                        placeholder='Enter a value...',
                        value='This is a TextArea component',
                        style={'width': '100%'}
                    )
            ], className="container-fluid",
                label="Product Highlight Generator")
        ], className="tabs-section")
    ], className="main-content"),
], className="main")

#Dropdown Callbacks
@app.callback(
    Output('multi-dropdown', 'options'),
    [Input('product-dropdown', 'value')])
def set_tags_options(selected_product):
    if DEBUG:
        print(selected_product)
    with open('data/{}.pkl'.format(str(selected_product)), 'rb') as handle:
        loaded_pkl = pickle.load(handle)
    tagged_df = loaded_pkl['tags_datasets']['USA'].columns[4:20]
    return [{'label': i, 'value': i} for i in tagged_df]

@app.callback(
    Output('multi-dropdown', 'value'),
    [Input('multi-dropdown', 'options')])
def set_tags_value(available_options):
    return available_options[0]['value']



#Meta Data Input
# @app.callback(Output('output-state', 'children'),
#               [Input('submit-button-state', 'n_clicks')],
#               [State('input-1-state', 'value'),
#                State('input-2-state', 'value')])
# def update_output(n_clicks, input1, input2):
#     return u'''
#         The Button has been pressed {} times,
#         Input 1 is "{}",
#         and Input 2 is "{}"
#     '''.format(n_clicks, input1, input2)


@app.callback(
    [Output('output_state', 'children'),
     Output(component_id='the_graph', component_property='figure')],
    [Input('run-operation', 'n_clicks'),
    Input('upload-image', 'contents'),
    Input('product-dropdown', 'value')],
    [State('product-length', 'value'),
     State('product-width', 'value'),
     State('product-height', 'value'),
     State('product-weight', 'value')]
)

def update_output(num_clicks,image_contents,selected_product,product_length,product_width,product_height,product_weight):
    if product_length is None:
        raise PreventUpdate
    elif product_width is None:
        raise PreventUpdate
    elif product_height is None:
        raise PreventUpdate
    elif product_weight is None:
        raise PreventUpdate
    else:
        temp_meta = np.array([float(product_length),float(product_height),float(product_width),float(product_weight)])
        meta_input = temp_meta.reshape(1,4,1,1)
        if image_contents is not None:
            print('Image contents found')
        image_b64 = image_contents[0].split(",")[1]
        base64_decoded = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(base64_decoded))
        image_np = np.array(image)
        target_size = (128,128)
        image_input = cv2.resize(image_np, target_size)
        print(image_input.shape)
        image_input = image_input.reshape(1,128,128,3)
        predictions_temp = {}
        with open('data/{}.pkl'.format(str(selected_product)), 'rb') as handle:
            loaded_pkl = pickle.load(handle)
        models = loaded_pkl['models']
        for country in models:
            predictions_temp.update({country:models[country].predict({'main_input': image_input, 'meta_input': meta_input})[0][0]})
        iso_changer = {'UK':'GBR','India':'IND','Australia':'AUS','USA':'USA'}
        df_temp = pd.DataFrame(data=predictions_temp.items(),columns = ['Country','Success Index'])
        df_temp['iso_alpha'] = df_temp['Country'].map(iso_changer)
        min_tar = min(df_temp['Success Index'])
        max_tar = max(df_temp['Success Index'])
        df_temp['Success Index'] = df_temp['Success Index'].apply(lambda x: scaling(x,1,10,min_tar,max_tar))
        df = df_temp.copy()
        print(df)
        fig = px.choropleth(df, locations="iso_alpha",
                            color="Success Index",
                            hover_name="Country",
                            projection='natural earth',
                            title='Performing Index of the Product by Country',
                            color_continuous_scale=px.colors.sequential.Plasma)

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))

        return ('High Index reflects that the product is likely to be successfull \
            if sold in that country',fig)

# @app.callback(Output('country-gdp-graph', 'figure'),
#               [Input('world-map', 'clickData')])
# def update_graph(clickData):
#     '''Update the carbon ppbv trend graph in Tab 1.
#     A callback function that is triggered when a country in the map in Tab 1 is
#     clicked. The country is retrieved from the clickData and is then used to
#     generate a line graph showing the trends in carbon ppbv of a country
#     across all years.
#     Parameters
#     ----------
#     clickData : dict
#         The dictionary containing the details of the clicked point on the map.
#     Returns
#     -------
#     dict
#         Return the updated carbon ppbv trend graph figure
#     '''
#     title = ''
#     data = []
#     if clickData:
#         country = clickData['points'][0]['location']
#     else:
#         country = 'USA'
#     data = [{'x': df.iloc[:, 1:].columns.tolist(),
#              'y': df.loc[country].iloc[1:].values.tolist(),
#              'type': 'line'}]
#     title = df.loc[country, 'country']
#     layout = dict(title='{} Carbon ppbv'.format(title),
#                   xaxis={'title': 'year'},
#                   yaxis={'title': 'Carbon ppbv'}
#                   )
#     fig = dict(data=data, layout=layout)
#     return fig
#
# image_source = "https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg"

@app.callback(Output('image_graph','figure'),
              [Input('upload-image', 'contents')])
def update_output(list_of_contents):
    if list_of_contents is not None:
        # if DEBUG:
        #     print(list_of_contents)
        image_b64 = list_of_contents[0].split(",")[1]
        base64_decoded = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(base64_decoded))
        image_np = np.array(image)
        fig = px.imshow(image_np)
        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
    else:
        image = Image.open(r'C:\Users\Dell-pc\Desktop\dash\images\ecfullfill.png')
        image_np = np.array(image)
        fig = px.imshow(image_np)
        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
    return fig
# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)

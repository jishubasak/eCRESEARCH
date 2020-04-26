import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.express as px

import os
import numpy as np
import pandas as pd
import logging

import plotly.graph_objs as go

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
from home.dash_apps.finished_apps import dash_reusable_components as drc
from home.dash_apps.finished_apps import utils as utils

# drc = importlib.import_module("dash_reusable_components")
# utils = importlib.import_module("utils")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

APP_PATH = 'C:/Users/Dell-pc/Desktop/Capstone/django/ecfullfill/home/dash_apps/finished_apps'

app = DjangoDash('SimpleExample')

app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

# resets the callbacks
app.callback_map = {}

# sets the title
app.title = 'Ecfullfill Capstone'

# html content
app.layout = html.Div([

                #Card Groups
            html.Div([
                #Product Length Button
                html.Div([
                    html.Div(id='output-container-button-1',
                             children='Enter Product Length'),
                    html.Div(dcc.Input(id='input-box-1', type='text'),
                        style={'position':'relative'}),
                    html.Button('Submit', id='button-1',
                        style={'position':'relative'})
                ],className='two columns'),
                #Product Width Button
                html.Div([
                    html.Div(id='output-container-button-2',
                             children='Enter Product Width'),
                    html.Div(dcc.Input(id='input-box-2', type='text',
                        style={'position':'relative'})),
                    html.Button('Submit', id='button-2',
                        style={'position':'relative'}),
                ],className='two columns'),
                #Product Height Button
                html.Div([
                    html.Div(id='output-container-button-3',
                             children='Enter Product Height'),
                    html.Div(dcc.Input(id='input-box-3', type='text',
                        style={'position':'relative'})),
                    html.Button('Submit', id='button-3',
                        style={'position':'relative'}),
                ],className='two columns'),
                #Product Weight Button
                html.Div([
                    html.Div(id='output-container-button-4',
                             children='Enter Product Weight'),
                    html.Div(dcc.Input(id='input-box-4', type='text')),
                    html.Button('Submit', id='button-4',
                        style={'position':'relative'}),
                ],className='two columns'),
                html.Div([
                    html.Div(id='output-container-button-5',
                             children='Enter Price'),
                    html.Div(dcc.Input(id='input-box-5', type='text',
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
                        options=[
                            {'label': 'Shampoo', 'value': 'shampoo'},
                            {'label': 'Conditioner', 'value': 'conditioner'},
                            {'label': 'Hair Oil', 'value': 'hair_oil'}
                        ],
                        value='shampoo'),
                ],className='six columns'),

                html.Div([
                    html.Div(id='output-container-button-7',
                             children='Select Tags'),

                    dcc.Dropdown(
                        options=[
                            {'label': 'Anti-Dandruff', 'value': 'anti_dandruff'},
                            {'label': 'Silky', 'value': 'silky'},
                            {'label': 'Argan Oil', 'value': 'argan_oil'}
                        ],
                        multi=True,
                        value="silky"),
                ],className='six columns')
            ],className='row'),

        html.Br(),
        html.Br(),
    # html.Div([
    #     html.Div(id='sub-header'),
    #     html.Br(),
    #     html.Div([
    #         html.Span(children='''Product Automation Tool Beta''')
    #
    #     ], id="intro"),
    # ], id='intro-section'),
    html.Div([
        dcc.Tabs([
            # Tab 1
            dcc.Tab([
                    #Upload COmponent
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
                            dcc.Input(id='input_state', type='number', inputMode='numeric', value=2007,
                                      max=2007, min=1952, step=5, required=True),
                            html.Button(id='submit_button', n_clicks=0, children='Run Operation'),
                            html.Div(id='output_state'),
                        ],style={'text-align': 'center'}),
                    ],className='six columns'),
            ], className="container-fluid", label="Dashboard 1"),



            # Tab 2
            dcc.Tab([
                    dcc.Textarea(
                        placeholder='Enter a value...',
                        value='This is a TextArea component',
                        style={'width': '100%'}
                    )
            ], className="container-fluid",
                label="Dashboard 2")
        ], className="tabs-section")
    ], className="main-content"),
], className="main")


@app.callback(
    [Output('output_state', 'children'),
    Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')]
)

def update_output(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        df = px.data.gapminder().query("year=={}".format(val_selected))
        # print(df[:3])

        fig = px.choropleth(df, locations="iso_alpha",
                            color="lifeExp",
                            hover_name="country",
                            projection='natural earth',
                            title='Life Expectancy by Year',
                            color_continuous_scale=px.colors.sequential.Plasma)

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))

        return ('The input value was "{}" and the button has been \
                clicked {} times'.format(val_selected, num_clicks), fig)

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
        if DEBUG:
            print(list_of_contents)
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

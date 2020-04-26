import datetime
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from PIL import Image
import base64
import io

DEBUG = True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div([
        dcc.Graph(id='the_graph')
    ]),
])


# def parse_contents(fig, filename, date):
#     return html.Div([
#         dcc.Graph(id='the_graph')
#     ])


@app.callback(Output('the_graph','figure'),
              [Input('upload-image', 'contents')])
def update_output(list_of_contents):
    if DEBUG:
        print(list_of_contents)
    image_b64 = list_of_contents[0].split(",")[1]
    base64_decoded = base64.b64decode(image_b64)
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)
    fig = px.imshow(image_np)
    fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                      margin=dict(l=60, r=60, t=50, b=50))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

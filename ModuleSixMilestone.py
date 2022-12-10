import dash
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output
from collections.abc import MutableMapping

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from main import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "useradmin"
password = "adminpwd"
shelter = AnimalShelter(username, password)

# class read method must support return of cursor object and accept projection json input
df = pd.DataFrame.from_records(shelter.read({}))

#########################
# Dashboard Layout / View
#########################
app = dash.Dash('CRUD')

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        # FIXME: Set up the features for your interactive data table to make it user-friendly for your client

    ),
    html.Br(),
    html.Hr(),
    html.Div(
        id='map-id',
        className='col s12 m6',
    )
])


#############################################
# Interaction Between Components / Controller
#############################################
# This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])

def update_map(viewData):
    dff = pd.DataFrame.from_dict(viewData)
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75, -97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            dl.Marker(position=[30.75, -97.48], children=[
                dl.Tooltip(dff.iloc[0, 4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[1, 9])
                ])
            ])
        ])
    ]


if __name__ == "__main__":
    app.run_server(debug=True)

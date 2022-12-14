import urllib
import dash
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# load data
from bson import Binary, Code
from bson.json_util import dumps

# TODO: import for their CRUD module
import main

df = pd.read_csv('aac_shelter_outcomes.csv')
# initialize app

# this is a dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
# the application interfaces are declared here
# this application has two input boxes, a submit button, a horizontal line and div for output
app.layout = html.Div(
    [
        dcc.Input(
            id="input_user".format("text"),
            type="text",
            placeholder="input type {}".format("text")),
        dcc.Input(
            id="input_passwd".format("password"),
            type="password",
            placeholder="input type {}".format("password")),
        html.Button('Execute', id='submit-val', n_clicks=0),
        html.Hr(),
        html.Div(id="query-out"),
        # TODO: insert unique identifier code here
        html.H1('William Harris Test Dash App', style={'textAlign': 'center'})
    ]
)


# this is area to define application responses or callback routines
# this one callback will take the entered text and if the submit button is clicked then call the
#  mongo database with the find_one query and return the result to the output div
@app.callback(
    Output("query-out", "children"),
    [Input("input_user".format("text"), "value"),
     Input("input_passwd".format("password"), "value"),
     Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input_passwd', 'value')]
)
def cb_render(userValue, passValue, n_clicks, buttonValue):
    if n_clicks > 0:
        ###########################
        # Data Manipulation / Model
        # use CRUD module to access MongoDB
        ##########################
        username = urllib.parse.quote_plus(userValue)
        password = urllib.parse.quote_plus(passValue)
        # TODO: Instantiate CRUD object with above authentication username and password values
        a = main.AnimalShelter(username, password)
        result = a.crud()

        # note that MongoDB returns BSON, the pyMongo JSON utility function dumps is used to convert to text
        # TODO: Return example query results
        return dumps(result)


if __name__ == "__main__":
    app.run_server(debug=True)

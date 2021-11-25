import time
import pathlib
import os

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import State, Input, Output
import dash_daq as daq

from dash import dcc, html

from app import app, server
from apps import lucy, jenny, gong, gong2
from apps import home

# Side panel
link_list = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link(dbc.Button('home', style={"width":"12em"}), href='/apps/home'),
    html.Br(),
    dcc.Link(html.Button('Model Performance', style={"width":"12em"}), href='/apps/lucy'),
    html.Br(),
    dcc.Link(html.Button('Vaccine Distribution', style={"width":"12em"}), href='/apps/gong'),
    html.Br(),
    dcc.Link(html.Button('Reported and Forcasted Death Cases', style={"width":"12em"}), href='/apps/gong2'),
    html.Br(),
    dcc.Link(html.Button('Model Explanation', style={"width":"12em"}), href='/apps/jenny')
])

dropdown_text = html.P(
    id="satellite-dropdown-text", children=["Dashboard"]
)

satellite_title = html.H1(id="satellite-name", children="We are")
satellite_body = html.P(
    className="satellite-description", 
    id="satellite-description", 
    children=[html.P("Han Gong (Duke MIDS)"),
            html.P("Lucy Lin (Duke Biostatistics)"),
            html.P("Jenny Zhuo (Duke Biostatistics)"),
            html.P("Junrong Lin (Duke Biostatistics)"),
            ],
    style={"font-style": "italic"}
)

side_panel_layout = html.Div(
    id="panel-side",
    children=[
        dropdown_text,
        html.Div(id="satellite-dropdown", children=link_list),
        html.Div(id="panel-side-text", children=[satellite_title, satellite_body])
    ],
)

app.layout = html.Div([
    side_panel_layout,
    html.Div(html.Div(id='page-content'))
], style={"display":"grid", "grid-template-columns": "1fr 5fr", "grid-gap": "20px"})

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/home' or pathname == '/':
        return home.layout
    elif pathname == '/apps/lucy':
        return lucy.layout
    elif pathname == '/apps/gong':
        return gong.layout
    elif pathname == '/apps/gong2':
        return gong2.layout
    elif pathname == '/apps/jenny':
        return jenny.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
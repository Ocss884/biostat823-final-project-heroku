import pandas as pd

import chart_studio.plotly as py
import plotly.offline as po

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from app import app

# Data processing forcasting death
forcast_death_df = pd.read_csv('https://raw.githubusercontent.com/Hannah-GOng/biostat823-covid19-analysis-project/main/dashboard/01_notebook/forecast_viz/2021-11-15-all-forecasted-deaths-model-data.csv')
forcast_death_df['forecast_date'] = pd.to_datetime(forcast_death_df['forecast_date']).dt.date
forcast_death_df = forcast_death_df[(forcast_death_df['target'] == '1 wk ahead cum death')|
                                    (forcast_death_df['target'] == '2 wk ahead cum death')|
                                    (forcast_death_df['target'] == '3 wk ahead cum death')|
                                    (forcast_death_df['target'] == '4 wk ahead cum death')]
# Data Processing Report
df_report = pd.read_csv('https://raw.githubusercontent.com/Hannah-GOng/biostat823-covid19-analysis-project/main/dashboard/01_notebook/forecast_viz/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')
df_abbrev = pd.read_csv('https://raw.githubusercontent.com/Hannah-GOng/biostat823-covid19-analysis-project/main/dashboard/01_notebook/forecast_viz/abbr-name.csv', header=None, names = ['state', 'location_name'])
df_report['submission_date'] = pd.to_datetime(df_report['submission_date']).dt.date
df_report = pd.merge(df_report, df_abbrev, on = 'state', how = 'inner')

layout = html.Div(
    children=[

html.Div(
    children=[
        html.Div(children = 'Location Name', style={'fontSize': "24px"},className = 'menu-title'),
        dcc.Dropdown(
                    id = 'location_name',
                    options = [
                        {'label': location_name, 'value':str(location_name)} for location_name in forcast_death_df['location_name'].unique()
                    ], # State Filter
                    value = 'North Carolina',
                    clearable = False,
                    searchable = False,
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
    className = 'menu',
),
        
html.Div(
    children=[
        html.Div(children = 'Forcasting Model', style={'fontSize': "24px"},className = 'menu-title'),
        dcc.Dropdown(
                    id = 'model',
                    options = [
                        {'label': model, 'value':str(model)} for model in ['BPagano', 'Ensemble', 'JHU-APL', 'USC', 'Microsoft', 'JHU-CSSE', 'Karlen']
                    ], # State Filter
                    value = 'Ensemble',
                    clearable = False,
                    searchable = False,
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
    className = 'menu',
),
        html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'forcast_case_graph',
                    figure = {},
                ),
                style={'width': '100%', 'display': 'inline-block'},
            ),
        ],
        className = 'graphs',
        ), 
    ]
)    

@app.callback(
    Output("forcast_case_graph", "figure"),
    Input("location_name", "value"), 
    Input("model", "value"))

def forcast_death_graph(location_name, model):
    
    # filter data   
    df_filter_death_forcast = forcast_death_df[forcast_death_df['model'] == model]
    df_filter_death_forcast = df_filter_death_forcast[df_filter_death_forcast['location_name'] == location_name]
    
    df_filter_report = df_report[df_report['location_name'] == location_name]
    df_filter_report = df_filter_report[(df_filter_report['submission_date'] <= pd.to_datetime('2021-11-15'))]
    df_filter_report = df_filter_report[(df_filter_report['submission_date'] > pd.to_datetime('2021-09-01'))]
    
    
    # death foresting
    fig_death = go.Figure([
        go.Scatter(
            name='Number of Death Forcasting',
            x = df_filter_death_forcast['target_week_end_date'],
            y = df_filter_death_forcast['point'],
            marker = dict(size=5),
            line=dict(color='rgb(250, 0, 0, 0.6)'),
        ),
        
        go.Scatter(
            name='Lower 50% Prediction Interval',
            x = df_filter_death_forcast['target_week_end_date'],
            y = df_filter_death_forcast['quantile_0.25'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name = 'Upper 50% Prediction Interval',
            x = df_filter_death_forcast['target_week_end_date'],
            y = df_filter_death_forcast['quantile_0.75'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='Lower 95% Prediction Interval',
            x = df_filter_death_forcast['target_week_end_date'],
            y = df_filter_death_forcast['quantile_0.025'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Upper 95% Prediction Interval',
            x = df_filter_death_forcast['target_week_end_date'],
            y = df_filter_death_forcast['quantile_0.975'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Bar(
            name='Number of Death Reported',
            x = df_filter_report['submission_date'],
            y = df_filter_report['tot_death'],
            
    ),
    ])
    
    fig_death.update_layout(
        yaxis_title='Number of Death',
        title='Reported and Forcast Number of Death By State',
        hovermode="x"
    )

    return fig_death
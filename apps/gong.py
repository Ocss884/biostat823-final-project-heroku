import pandas as pd
from sodapy import Socrata
import chart_studio.plotly as py
import plotly.offline as po
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
from app import app
from dash import dcc, html
from dash.dependencies import Input, Output

client = Socrata("data.cdc.gov", None)
results = client.get("unsk-b7fc", limit = 200000)
df = pd.DataFrame.from_records(results)
df['date'] = pd.to_datetime(df['date']).dt.date
df['distributed_janssen'] = df['distributed_janssen'].astype(int)
df['distributed_moderna'] = df['distributed_moderna'].astype(int)
df['distributed_pfizer'] = df['distributed_pfizer'].astype(int)
df['distributed'] = df['distributed'].astype(int)
# filter states

abbr_state = pd.read_csv('https://raw.githubusercontent.com/Hannah-GOng/biostat823-covid19-analysis-project/main/data/abbr-name.csv', header = None)
df = df[df['location'].isin(abbr_state[0])]
df['location'].unique()

layout = html.Div(
    children=[

html.Div(
    children=[
        html.Div(children = 'state', style={'fontSize': "24px"},className = 'menu-title'),
        dcc.Dropdown(
                    id = 'state',
                    options = [
                        {'label': state, 'value':str(state)} for state in df['location'].unique()
                    ], # State Filter
                    value = 'NC',
                    clearable = False,
                    searchable = False,
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
    className = 'menu',
),
        
html.Div(
    children=[
        html.Div(children = 'date-picker-range', style={'fontSize': "24px"},className = 'menu-title'),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed = df['date'].min(),
            max_date_allowed = df['date'].max(),
            initial_visible_month = df['date'].max(),
            end_date = df['date'].max(),
            start_date = df['date'].min(),
            start_date_placeholder_text="Start Period",
            end_date_placeholder_text="End Period",
            calendar_orientation='vertical'  
        ),
            ],
    className = 'menu',
),
    
        html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'daily_distribution',
                    figure = {},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'type_distribution',
                    figure = {},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'recipients',
                    figure = {},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
        ],
        className = 'double-graphs',
        ), 
    ]
)    
@app.callback(
    Output("daily_distribution", "figure"),
    Input("date-picker-range", "start_date"), 
    Input("date-picker-range", "end_date"),
    Input("state", "value"))

def distribution_by_location_date(start_date, end_date, state):
    df_filter = df[df['date'] == pd.to_datetime(end_date)]
    
    fig_geo = go.Figure(data = go.Choropleth(
    locations = df_filter['location'],
    z = df_filter['distributed'],
    locationmode='USA-states',
    colorscale='Blues',
    autocolorscale=False,
    text = df['location'],
    marker_line_color='white',
    colorbar_title="Daily Number of Vaccine Distributed"
    ))

    fig_geo.update_layout(
        title_text='Number of Vaccine Distributed',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),)

    return fig_geo

@app.callback(
    Output("type_distribution", "figure"), 
    Input("date-picker-range", "start_date"), 
    Input("date-picker-range", "end_date"),
    Input("state", "value"))

def distribution_compare(start_date, end_date, state):
    df_filter = df[df['date'] <= pd.to_datetime(end_date)]
    df_filter = df_filter[df_filter['date'] >= pd.to_datetime(start_date)]
    df_filter = df_filter[df_filter['location'] == state]
    
    fig_compare = make_subplots(rows=2, cols=2)
    
    fig_compare.add_trace(go.Bar(x = df_filter['date'],
                                     y = df_filter['distributed_janssen'],
                                     name = "J&J"),
                         row=1, col=1)
    
    fig_compare.add_trace(go.Bar(x = df_filter['date'],
                                     y = df_filter['distributed_moderna'],
                                     name = 'moderna'),
                         row=1, col=2)
    
    fig_compare.add_trace(go.Bar(x = df_filter['date'],
                                         y = df_filter['distributed_pfizer'],
                                         name = 'pfizer'),
                         row=2, col=1)
    
    fig_compare.add_trace(go.Bar(x = df_filter['date'],
                                         y = df_filter['distributed_pfizer'] + df_filter['distributed_moderna'] + df_filter['distributed_janssen'],
                                         name = 'ALL'),
                         row=2, col=2)
    
    fig_compare.update_yaxes(range=[0, 15000000])
    fig_compare.update_layout(title_text='Vaccine Distribution Trend')  
    return fig_compare

@app.callback(
    Output("recipients", "figure"), 
    Input("date-picker-range", "start_date"), 
    Input("date-picker-range", "end_date"),
    Input("state", "value"))
  
def number_of_recipients(start_date, end_date, state):
    
    df['administered_dose1_pop_pct'] = df['administered_dose1_pop_pct'].astype(float)
    df['series_complete_pop_pct'] = df['series_complete_pop_pct'].astype(float)
    df['additional_doses_vax_pct'] = df['additional_doses_vax_pct'].astype(float)
    
    df_filter = df[df['date'] <= pd.to_datetime(end_date)]
    df_filter = df_filter[df_filter['date'] >= pd.to_datetime(start_date)]
    df_filter = df_filter[df_filter['location'] == state]
    
    fig_pct = make_subplots(rows=2, cols=2)
    
    fig_pct.add_trace(go.Bar(x = df_filter['date'],
                                     y = df_filter['administered_dose1_pop_pct'],
                                     name = "pct_recieved_at_least_one_dose"),
                         row=1, col=1)
    
    fig_pct.add_trace(go.Bar(x = df_filter['date'],
                                     y = df_filter['series_complete_pop_pct'],
                                     name = 'pct_fully_vaccinated'),
                         row=1, col=2)
    
    fig_pct.add_trace(go.Bar(x = df_filter['date'],
                                     y = df_filter['additional_doses_vax_pct'],
                                     name = 'pct_recieved_booster'),
                         row=2, col=1)
    
    
    fig_pct.update_layout(title_text='Percentage of Vaccinated Population')  
    return fig_pct
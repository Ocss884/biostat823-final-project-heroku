import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from pandas_datareader import data as web
import plotly.graph_objs as go
import pandas as pd
import json
import plotly.express as px
from dash import dash_table as dt
import plotly.figure_factory as ff
import numpy as np
import os
from app import app

data = pd.read_csv("https://raw.githubusercontent.com/Hannah-GOng/biostat823-covid19-analysis-project/main/data/model_results_final.csv")

metric_filter = data['variable'].unique()
method_filter = data['Method'].unique()
model_filter = data['Model'].unique()
layout = html.Div([
    html.Div([
        html.Div([
                html.Div([      
                    
                    html.H2('Dashboard1: Performance of Classification Model by Methods and Metrics', style=dict(color='#7F90AC')),
                    ], className = "nine columns padded" )
            ], className = 'row gs-header gs-text-header'),
       html.Div([

        html.Div([
            dcc.Dropdown(
                id='metric_filter',
                options=[{'label': i, 'value': i} for i in metric_filter],
                value='Accuracy'
            )
        ],style={'width': '40%', 'display': 'inline-block','align-items': 'center','justify-content': 'center','margin-left': '5%'}),
        html.Div([
            dcc.Dropdown(
                id='method_filter',
                options=[{'label': i, 'value': i} for i in method_filter],
                value='Dataset after Deleting all the NAs'
            )
        ],
        style={'width': '40%', 'display': 'inline-block','align-items': 'center','justify-content': 'center','margin-left': '10%'})
    ]),
    html.Div([
        html.Div([
        dcc.Graph(
            id='method-filter-scatter',
            hoverData={'points': [{'customdata': 'Ridge Classifier'}]}
        )],style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
        dcc.Graph(
            id = 'confusion_matrix1')
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})
    ])
    ],className = 'page'),
    # Page 2
     html.Div([
        html.Div([
                html.Div([      
                    
                    html.H2('Dashboard2: Performance of Classification Model by Models and Metrics', style=dict(color='#7F90AC')),
                    ], className = "nine columns padded" )
            ], className = 'row gs-header gs-text-header'),
       html.Div([
         html.Div([
            dcc.Dropdown(
                id='metric_filter1',
                options=[{'label': i, 'value': i} for i in metric_filter],
                value='Accuracy'
            )
            ],style={'width': '40%', 'display': 'inline-block','margin-left': '5%'}),
         html.Div([
            dcc.Dropdown(
                id='model_filter',
                options=[{'label': i, 'value': i} for i in model_filter],
                value='Ridge Classifier',
            )
            ],style={'width': '40%', 'display': 'inline-block','margin-left': '10%'} )
        
    ]),
    html.Div([
        html.Div([
        dcc.Graph(
            id='model-filter-scatter',
            hoverData={'points': [{'customdata':'Dataset after Deleting all the NAs'}]}
        )
        ], style={'width': '49%', 'display': 'inline-block','align-items': 'center','justify-content': 'center'}),
        html.Div([
        dcc.Graph(
            id='confusion_matrix'
        )
        ], style={'width': '49%', 'display': 'inline-block',  'align-items': 'center','justify-content': 'center'})
    ])
    ],className = 'page'),
])
@app.callback(
    dash.dependencies.Output('method-filter-scatter', 'figure'),
    [dash.dependencies.Input('method_filter', 'value'),
     dash.dependencies.Input('metric_filter','value')]
    ) 
def update_graph1(selected_methods,selected_metrics):
    filtered_df = data[(data['variable'] == selected_metrics) & (data['Method'] == selected_methods)]
    return {
        'data':[go.Scatter(
           x = filtered_df['Model'],
           y = filtered_df['value'],
           text = filtered_df['Model'],
           customdata = filtered_df['Model']
           #marker_color=colors
        )],
        'layout': go.Layout(
           
           yaxis={
               'title': 'Score'
           },
           height = 450,
           hovermode = 'closest',
           title = '<b>Performance of Classifier<b>'
        )
    }

def create_cm(dff):
    dff = dff.drop(['Method','Model','variable','value'],axis = 1)
    arr = np.zeros((2, 2), dtype=np.int)
    matrix = dff.values
    arr[0,0] = matrix[0,0]
    arr[0,1] = matrix[0,1]
    arr[1,0] = matrix[0,2]
    arr[1,1] = matrix[0,3]
    x = ['deceased','discharged']
    y = ['deceased','discharged']
    z_text = [[str(y) for y in x] for x in arr]
    fig = ff.create_annotated_heatmap(arr, x=x, y=y, annotation_text=z_text, colorscale=['aliceblue','aqua','aquamarine','darkturquoise'])
    fig.update_layout(title_text='<i><b>Confusion matrix</b></i>',
                  #xaxis = dict(title='x'),
                  #yaxis = dict(title='x')
                 )
    return fig
@app.callback(
    dash.dependencies.Output('confusion_matrix1', 'figure'),
    [dash.dependencies.Input('method_filter', 'value'),
     dash.dependencies.Input('method-filter-scatter','hoverData')
    ]) 
def update_cm_graph(selected_methods,hoverData):
    model_name = hoverData['points'][0]['customdata']
    dff = data[(data['Model'] == model_name) & (data['Method'] == selected_methods)]
    return create_cm(dff)
    
@app.callback(
    dash.dependencies.Output('model-filter-scatter', 'figure'),
    [dash.dependencies.Input('model_filter', 'value'),
     dash.dependencies.Input('metric_filter1','value')]
    ) 
def update_graph(selected_models,selected_metrics):
    filtered_df = data[(data['variable'] == selected_metrics) & (data['Model'] == selected_models)]
    return {
        'data':[go.Scatter(
           x = filtered_df['Method'],
           y = filtered_df['value'],
           text = filtered_df['Method'],
           customdata = filtered_df['Method']
           #marker_color=colors
        )],
        'layout': go.Layout(
           
           yaxis={
               'title': 'Data_Preprocessing_Method '
           },
           height = 450,
           hovermode = 'closest',
           title = '<b>Performance of Data Preprocessing Method<b>'
        )
    }
@app.callback(
    dash.dependencies.Output('confusion_matrix', 'figure'),
    [dash.dependencies.Input('model_filter', 'value'),
     dash.dependencies.Input('model-filter-scatter','hoverData')
    ]) 
def update_cm_graph(selected_models,hoverData):
    model_name = hoverData['points'][0]['customdata']
    dff = data[(data['Method'] == model_name) & (data['Model'] == selected_models)]
    return create_cm(dff)
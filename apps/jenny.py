import dash as dash
from dash import dcc, html
import flask as flask
import glob as glob
import os as os
from app import app

image_directory = 'https://raw.githubusercontent.com/Hannah-GOng/biostat823-covid19-analysis-project/main/dashboard/02_images/'
dropdown_images = {
    "shap_pic_base.png": "Dataset after Deleting all the NAs",
    "shap_pic_im.png": "Dataset after Missing Data Imputation",
    "shap_pic_imb.png": "Dataset after Dealing with Imbalance",
    "shap_pic_db.png": "Dataset after Missing Data Imputation and Dealing with Imbalance"
}
list_of_images = [image_directory+x for x in list(dropdown_images.keys())]

layout = html.Div([
    dcc.Dropdown(
        id = 'image-dropdown',
        options = [{'label': v, 'value': k} 
                   for k, v in dropdown_images.items()],
        value = "shap_pic_base.png",
        style = dict(
        width = '70%',
        verticalAligh = 'middle')
    ),
    html.Img(id = 'image',
             style = {'width': '150vh', 'height': '80vh'})
])

@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('image-dropdown', 'value')])
def update_image_src(value):
    return image_directory+value
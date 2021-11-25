import dash
from dash import dcc, html
from app import app

layout = html.Div([html.H1(id="satellite-introduction", children="Introduction", style={"color": "#fec036"}),
html.P("This dashboard provides an overview of several essential aspects of the current COVID-19 situation: vaccinations, new cases, and deaths. Page one and two can be helpful to the consumers who are interested in knowing the estimated new cases for the next few weeks, learning about the trend of new cases, and detecting possible correlation between vaccinations and new cases. Meanwhile, page three is informative to the consumers who are curious about which factors may contribute more to the deaths of COVID-19 positive patients. Therefore, this dashboard makes the above information more simple and intuitive to find and understand.", style={"font-size":"16pt"})
],style={"padding":"4em"})

from dash import Dash, html, dcc, Input, Output, ctx
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from shapely.geometry import Point

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])


header = html.Div("Arapahoe Covid-19 Case Investigation Tool", className="h2 p-2 text-white bg-primary text-center")
bgcolor = "#f3f3f1"  # mapbox light map land color
template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}

def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "template": template,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }

app.layout = dbc.Container([
    header,
    # dbc.Row(dcc.Graph(id='ct-map', figure=blank_fig(500))),
    # dbc.Row([
    #         dbc.Col([
    #             dcc.Slider(0, 1, value=1,
    #                 marks={
    #                     0: {'label': 'Light', 'style': {'color': 'white'}},
    #                     1: {'label': 'Dark', 'style': {'color': 'white'}},
    #                 },
    #                 id = 'opacity',
    #             ),
    #         ], width=2),
    #         dbc.Col([
    #             dcc.Checklist(
    #                 id='tract-radio',
    #                 options=[
    #                     {'label': 'Uninsured', 'value': 'F_UNINSUR'},
    #                     {'label': 'Poverty', 'value': 'F_POV150'},
    #                 ],
    #             ),
    #         ], width=2),
    #     ]),      
    #     dcc.Store(id='pov-data', storage_type='memory'),
    #     dcc.Store(id='ins-data', storage_type='memory'),
    #     dcc.Store(id='case-data', storage_type='memory'),
])  

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
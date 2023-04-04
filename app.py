from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

header = html.Div("Arapahoe Covid-19 Case Investigation Tool", className="h2 p-2 text-white bg-primary text-center")

df = pd.read_csv('/Users/jamesswank/Downloads/CSV.csv')
print(df)


app.layout = dbc.Container([
    header,
])


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
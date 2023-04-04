from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])


bgcolor = "#f3f3f1"  # mapbox light map land color
header = html.Div("Arapahoe Covid-19 Case Investigation Tool", className="h2 p-2 text-white bg-primary text-center")
template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}


df = pd.read_csv('/Users/jamesswank/Downloads/CSV.csv')
# print(df)

gdf_2020 = gpd.read_file('2020_CT/ArapahoeCT.shp')
# gdf_2020['FIPS'] = gdf_2020['FIPS'].apply(lambda x: x[5:])
# print(gdf_2020['FIPS'])

df_SVI_2020 = pd.read_csv('Colorado_SVI_2020.csv')
df_SVI_2020 = df_SVI_2020.loc[df_SVI_2020['COUNTY'] == 'Arapahoe']

col_list = list(df_SVI_2020)

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
    dbc.Row(dcc.Graph(id='ct-map', figure=blank_fig(500))),
    dbc.Row([
            dbc.Col([
                dcc.Slider(0, 1, value=1,
                    marks={
                        0: {'label': 'Light', 'style': {'color': 'white'}},
                        1: {'label': 'Dark', 'style': {'color': 'white'}},
                    },
                    id = 'opacity',
                ),
            ], width=2),
            dbc.Col([
                dcc.RadioItems(
                    id='category-radio',
                    options=[
                        {'label': 'Total', 'value': 'E_'},
                        {'label': 'Pct.', 'value': 'EP_'},
                        {'label': 'Percentile', 'value': 'EPL_'},
                        {'label': 'Flag', 'value': 'F_'},
                    ],
                    value='F_' 
                ),
            ], width=2),
            dbc.Col([
                dcc.Dropdown(
                    id='variable-dropdown',
                ),
            ], width=2)
        ]),
])

@app.callback(
        Output('variable-dropdown', 'options'),
        Input('category-radio', 'value')
)
def category_options(selected_value):
    print(selected_value)
    # variables = list(lambda x: x, col_list)
    variables = [{'label': i, 'value': i} for i in list(filter(lambda x: x.startswith(selected_value), col_list))]
    # print([{'label': i, 'value': i} for i in col_list[filter(lambda x: x.startswith(selected_value))]])
    return variables 


@app.callback(
    Output('ct-map', 'figure'),
    # Input('year-map-data', 'data'),
    Input('variable-dropdown', 'value'),
    # Input('year', 'value'),
    Input('opacity', 'value')
)
def get_figure(variable, opacity):
  
    df.rename(columns={'tract2000':'FIPS'}, inplace=True)
    df['FIPS'] = df["FIPS"].astype(str)
    df_SVI_2020['FIPS'] = df_SVI_2020["FIPS"].astype(str)
    selected_tracts = df_SVI_2020.loc[df_SVI_2020[variable] == 1]
    tgdf = gdf_2020.merge(selected_tracts, on='FIPS')
    # print(df_SVI_2020['FIPS'])
    tgdf = tgdf.set_index('FIPS')
    # print(tgdf.columns)
    # print(tgdf)
    
    print(selected_tracts)

    
    
    fig=go.Figure()

    fig.add_trace(go.Scattermapbox(
            lat=df['geocoded_latitude'],
            lon=df['geocoded_longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10,
                color='red'
            )
    ))
                                            
  

    fig2 = px.choropleth_mapbox(tgdf, 
                                geojson=tgdf.geometry, 
                                color=variable,                               
                                locations=tgdf.index, 
                                # featureidkey="properties.TRACTCE20",
                                opacity=opacity)
    
    fig.add_traces(list(fig2.select_traces()))

    fig.update_layout(mapbox_style="carto-positron", 
                      mapbox_zoom=10.4,
                      mapbox_center={"lat": 39.65, "lon": -104.8},
                      margin={"r":0,"t":0,"l":0,"b":0},
                      uirevision='constant')


    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
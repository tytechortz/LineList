from dash import Dash, html, dcc, Input, Output, ctx
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])


header = html.Div("Arapahoe Covid-19 Case Investigation Tool", className="h2 p-2 text-white bg-primary text-center")
bgcolor = "#f3f3f1"  # mapbox light map land color
template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}

gdf_2020 = gpd.read_file('2020_CT/ArapahoeCT.shp')
gdf_2020 = gdf_2020.to_crs('WGS84')
gdf_2020['FIPS'] = gdf_2020['FIPS'].apply(lambda x: x[4:])

df_SVI_2020 = pd.read_csv('Colorado_SVI_2020.csv')
df_SVI_2020 = df_SVI_2020.loc[df_SVI_2020['COUNTY'] == 'Arapahoe']
df_SVI_2020['FIPS'] = df_SVI_2020["FIPS"].astype(str)
df_SVI_2020['FIPS'] = df_SVI_2020['FIPS'].apply(lambda x: x[4:])

df = pd.read_csv('/Users/jamesswank/Downloads/CSV.csv')

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
                dcc.Checklist(
                    id='tract-radio',
                    options=[
                        {'label': 'Uninsured', 'value': 'F_UNINSUR'},
                        {'label': 'Poverty', 'value': 'F_POV150'},
                    ],
                ),
            ], width=2),
        ]),      
        dcc.Store(id='variable-data', storage_type='session'),
])  

@app.callback(
    Output('variable-data', 'data'),
    Input('tract-radio', 'value'))
def get_tract_data(variable):

    tgdf = gdf_2020.merge(df_SVI_2020, on='FIPS')

    for i in variable:
        # print(variable)
        df_UI = tgdf.loc[tgdf['F_UNINSUR'] == 1]
        df_Pov = tgdf.loc[tgdf['F_POV150'] == 1]

    return(print(variable))

@app.callback(
    Output('ct-map', 'figure'),
    # Input('all-map-data', 'data'),
    Input('variable-data', 'data'),
    Input('opacity', 'value')
)
def get_figure(var_data, opacity):

    fig=go.Figure()

    print(var_data)

    tgdf = gdf_2020.merge(df_SVI_2020, on='FIPS')

    df_UI = tgdf.loc[tgdf['F_UNINSUR'] == 1]
    df_Pov = tgdf.loc[tgdf['F_POV150'] == 1]

    # for i in variable:
    #     fig.add_trace(go.Choroplethmapbox(
    #         geojson=eval(df_UI['geometry'].to_json()),
    #         locations=df_UI.index,
    #         z=df_UI[i],
    #         # coloraxis='coloraxis',
    #         colorscale=([0,'rgba(0,0,0,0)'],[1, 'lightgreen']),
    #         zmin=0,
    #         zmax=1,
    #     ))

    fig.add_trace(go.Scattermapbox(
                    lat=df['geocoded_latitude'],
                    lon=df['geocoded_longitude'],
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        size=10,
                        color='red'
                    )
            ))
    



    fig.update_layout(mapbox_style="carto-positron", 
                        mapbox_zoom=10.4,
                        #   mapbox_layers=layer,
                        mapbox_center={"lat": 39.65, "lon": -104.8},
                        margin={"r":0,"t":0,"l":0,"b":0},
                        uirevision='constant',
                        ),


    return fig




if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
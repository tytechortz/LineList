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


gdf_2020 = gpd.read_file('2020_CT/ArapahoeCT.shp')
gdf_2020 = gdf_2020.to_crs('WGS84')
# gdf_2020['FIPS'] = gdf_2020["FIPS"].astype(str)
gdf_2020['FIPS'] = gdf_2020['FIPS'].apply(lambda x: x[4:])
case_df = pd.read_csv('/Users/jamesswank/Downloads/CSV.csv')

df_SVI_2020 = pd.read_csv('Colorado_SVI_2020.csv')
df_SVI_2020 = df_SVI_2020.loc[df_SVI_2020['COUNTY'] == 'Arapahoe']
df_SVI_2020['FIPS'] = df_SVI_2020["FIPS"].astype(str)
df_SVI_2020['FIPS'] = df_SVI_2020['FIPS'].apply(lambda x: x[4:])

df_pov=df_SVI_2020.loc[df_SVI_2020['F_POV150']==1]
    
df_pov['FIPS'] = df_pov["FIPS"].astype(str)

df_uninsur=df_SVI_2020.loc[df_SVI_2020['F_UNINSUR']==1]
   
df_uninsur['FIPS'] = df_uninsur["FIPS"].astype(str)


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
        dcc.Store(id='pov-data', storage_type='memory'),
        dcc.Store(id='ins-data', storage_type='memory'),
    #     dcc.Store(id='case-data', storage_type='memory'),
])  

@app.callback(
    Output('pov-data', 'data'),
    Input('tract-radio', 'value'))
def get_tract_data(variable):

    df_pov=df_SVI_2020.loc[df_SVI_2020['F_POV150']==1]
    
    df_pov['FIPS'] = df_pov["FIPS"].astype(str)

    if 'F_POV150' in variable:
        return df_pov.to_json()


@app.callback(
    Output('ins-data', 'data'),
    Input('tract-radio', 'value'))
def get_tract_data(variable):

    df_uninsur=df_SVI_2020.loc[df_SVI_2020['F_UNINSUR']==1]
   
    df_uninsur['FIPS'] = df_uninsur["FIPS"].astype(str)
   
    if 'F_UNINSUR' in variable:
        return df_uninsur.to_json()


@app.callback(
    Output('ct-map', 'figure'),
    Input('tract-radio', 'value'),
    Input('opacity', 'value'),
    Input('pov-data', 'data'),
    Input('ins-data', 'data'))
def get_figure(variable, opacity, pov, ins):
    print(variable)
    
    fig=go.Figure()
    
    if variable:
        if any(x in variable for x in ['F_POV150', 'F_UNINSUR']):
            # df_pov = pd.read_json(pov)
            # df_pov['FIPS'] = df_pov["FIPS"].astype(str)
            # df_ins = pd.read_json(ins)
            # df_ins['FIPS'] = df_ins["FIPS"].astype(str)
            for i in variable:
                
                df=df_SVI_2020.loc[df_SVI_2020[i]==1] 
                tgdf = gdf_2020.merge(df, on='FIPS')
                fig.add_trace(go.Choroplethmapbox(
                    geojson=eval(tgdf['geometry'].to_json()),
                                    locations=tgdf.index,
                                    z=tgdf[i],
                                    # coloraxis='coloraxis',
                                    marker={'opacity':opacity},
                                    colorscale=([0,'rgba(0,0,0,0)'],[1, 'lightblue']),
                                    zmin=0,
                                    zmax=1,
                                    showscale=False,
                ))
    

    fig.add_trace(go.Scattermapbox(
                    lat=case_df['geocoded_latitude'],
                    lon=case_df['geocoded_longitude'],
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        size=10,
                        color='red',
                    ),
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
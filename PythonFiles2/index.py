"""
This is a basic multi-page Dash app using Bootstrap.
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_cytoscape as cyto

import os

os.chdir("/Users/victormartinez/Projects/FINNET-Dash/PythonFiles/")

import src.components.navbar as nb
import src.components.sidebar as sb
import pyTigerGraph as tg
import plotly.express as px
import json
import pandas as pd
import numpy as np
import connect
import threading

dataLock = threading.Lock()
conn = connect.getConnection()

import src.pages.assetView as p1
import src.pages.mapExplore as p3
import src.pages.dataStatistics as p4
import src.pages.compositionView as p2
import src.pages.about as p5
import time 
from dash.dependencies import Input, Output, State
from datetime import datetime , timedelta 
from config import graphistry_un, graphistry_pw
import operator
import keplergl

import plotly.graph_objects as go
import plotly.express as px


# link fontawesome to get the chevron icons
FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

# setup stylesheets
app = dash.Dash(external_stylesheets=[dbc.themes.LUX, FA])

'''
TigerGraph Connection Parameters:
'''

# conn = connect.getConnection()
def Setup_pages(conn,graphistry_un,graphistry_pw):
    # setup parameters
    navbar = nb.get_navbar()
    sidebar = sb.get_sidebar()
    assetView = p1.get_page(conn)
    compositionView = p2.get_page(conn,graphistry_un,graphistry_pw)
    mapView = p3.get_page(conn)
    dataView = p4.get_page(conn)
    aboutView = p5.get_page()
    return navbar , sidebar , assetView , compositionView , mapView  , dataView ,  aboutView



# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def generateKeplerMap():
#    q = conn.runInstalledQuery("getAllTravel")
#    df = pd.json_normalize(q[0]['Seed'])
    df = pd.read_csv('../Data/kepler-gl_new dataset.csv')
    # print(df)
    map_1 = keplergl.KeplerGl()
    map_1.add_data(data=df)
    if not os.path.isfile('finnet_map.html'):
        map_1.save_to_html(file_name="finnet_map.html")
    else:
#        os.remove('Dash-Bootstrap-TigerGraph-Covid19/covid_map.html')
        map_1.save_to_html(file_name="finnet_map.html")

    kep_viz = html.Iframe(srcDoc=open('finnet_map.html').read(),
                          height='800', width='100%')
    return kep_viz


@app.callback(Output('output-map', 'children'), [Input(component_id="map-button", component_property="n_clicks")])
def generateMap(n_clicks):
    if n_clicks > 0:
        try:
            map = generateMap()
            return map
        except Exception as e:
            return [html.Br(), html.P("Uh oh", style={'color': 'red'})]


def getAssetData(userID):
    userID = userID.strip()       
    q = conn.runInstalledQuery("get_asset_value", {'p': userID})
    assetID = q[0]['asset'][0]['v_id']
    assetName = q[0]['asset'][0]['attributes']['name']
    assetSymbol = q[0]['asset'][0]['attributes']['symbol']
    assetCusip = q[0]['asset'][0]['attributes']['cusip']
    assetCountry = q[0]['asset'][0]['attributes']['region']
    assetCurrency = q[0]['asset'][0]['attributes']['currency']
    assetIndustry = q[0]['asset'][0]['attributes']['type']
    assetLocation = q[0]['asset'][0]['attributes']['location']
    assetExchange = q[0]['asset'][0]['attributes']['exchange']
    assetDescription = q[0]['asset'][0]['attributes']['description']

#    patientAge = datetime.now().year - patientBirthYear
#    patientActive = False if q[0]['Patient'][0]['attributes']['deceased_date'].startswith(
#        '1970') else True

    assetActive = True

    sdate = np.array([q[0]['valueall'][i]['attributes']['sdate'] for i in range(len(q[0]['valueall']))])
    indx_t = np.argsort(sdate)
    
    assetEarliestV = sdate[indx_t[0]]
    assetLatestV = sdate[indx_t[len(q[0]['valueall'])-1]]    
    
    return assetName, assetSymbol, assetCusip, assetDescription, assetCountry, assetCurrency, assetIndustry, assetLocation, assetExchange, assetActive, assetEarliestV, assetLatestV


def getAssetDates(userID):
    userID = userID.strip()       
    q = conn.runInstalledQuery("get_asset_value", {'p': userID})
    # print(str(q))
    # patientDates = []
    # patientDateLabels = []
    divs = []
    dates = []

    x = np.array([q[0]["valueall"][i]["attributes"]["liquid_price"] for i in range(len(q[0]["valueall"]))])
    t = np.array([q[0]["valueall"][i]["attributes"]["sdate"] for i in range(len(q[0]["valueall"]))])

    i_sort = np.argsort(t)    

    i_max = np.argmax(x)
    i_min = np.argmin(x)
    
    i_last = i_sort[len(i_sort)-1]
    
    i_beggin = i_sort[0]

    i_middle = (np.abs(x - (x[i_max]+x[i_min])/2)).argmin()

    tmp_str = t[i_min]
    date = tmp_str.split(' ')
    dates.append(
        [date[0], " | MIN: ",  f"{x[i_min]}", 'fa fa-medkit fa-lg', 'red'])

    tmp_str = t[i_max]
    date = tmp_str.split(' ')
    dates.append(
        [date[0], "| MAX: ", f"{x[i_max]}", 'fa fa-plane fa-lg', 'black'])

    tmp_str = t[i_beggin]
    date = tmp_str.split(' ')
    dates.append(
        [date[0], " | MIN: ", f"{x[i_beggin]}", 'fa fa-plane fa-lg', 'black'])


    tmp_str = t[i_last]
    date = tmp_str.split(' ')
    dates.append(
        [date[0], " | End: ", f"{x[i_last]}", 'fa fa-plane fa-lg', 'black'])


    dates.sort(key=operator.itemgetter(0, 1))
    # print(dates)
    for x in dates:
        # print(x[0], x[1])
        # f"Date: 2020-{x[0]}-{x[1]}"
        divs.append(
            dbc.Row(
                [
                    html.I(
                        className=f"{x[3]}",
                        style={'margin-left': '5px',
                               'margin-right': '5px', 'color': f"{x[4]}"},
                    ),
                    html.H5(
                        f"{x[0]}-{x[1]} | {x[2]}",
                        # style={'color': f"{x[4]}"}
                    )
                ]
            )

        )
        divs.append(html.Hr(style={'margin': '0 0 1.24rem 0'}))

    return divs


def getAssetStats(userID):
    userID = userID.strip()       
    q = conn.runInstalledQuery("get_asset_value", {'p': userID})

    x = np.array([q[0]["valueall"][i]["attributes"]["liquid_price"] for i in range(len(q[0]["valueall"]))])
    t = np.array([q[0]["valueall"][i]["attributes"]["sdate"] for i in range(len(q[0]["valueall"]))])

    i_sort = np.argsort(t)    

    logR = np.diff(np.log(x[i_sort]))        

    vol_30 = np.std(logR[len(logR) - 30:len(logR)-1])*np.sqrt(360/30)    
    vol_60 = np.std(logR[len(logR) - 60:len(logR)-1])*np.sqrt(360/60)
    vol_180 = np.std(logR[len(logR) - 180:len(logR)-1])*np.sqrt(360/180)
    vol_all = np.std(logR)*np.sqrt(360/len(logR))

    return [vol_30, vol_60, vol_180, vol_all]


@app.callback([Output('vol-30-div', 'children'), Output('vol-60-div', 'children'), Output('vol-180-div', 'children'), Output('vol-all-div', 'children')], [Input(component_id="input-group-button", component_property="n_clicks")], [State("input-group-button-input", "value")])
def getassetStats(n_clicks, userID):
    userID = userID.strip()       
    if n_clicks != 0:
        try:
            results = getAssetStats(userID)
            return [html.Div(
                [
                    html.P('Volatility 30d'),
                    html.Br(),
                    html.P("{:.2f}".format(results[0]*100)+'%'),
                ],
            ),
                html.Div(
                [
                    html.P('Volatility 60d'),
                    html.Br(),
                    html.P("{:.2f}".format(results[1]*100)+'%'),
                ]
            ),
                html.Div(
                [
                    html.P('Volatility 180d'),
                    html.Br(),
                    html.P("{:.2f}".format(results[2]*100)+'%'),
                ]
            ),
                html.Div(
                [
                    html.P('Valatility All'),
                    html.Br(),
                    html.P("{:.2f}".format(results[3]*100)+'%'),
                ]
            )]
        except Exception as e:
            return html.P("Error", style={'color': 'red'}), html.P("Error", style={'color': 'red'}), html.P("Error", style={'color': 'red'}), html.P("Error", style={'color': 'red'})


@app.callback(Output('timeline-div', 'children'), [Input(component_id="input-group-button", component_property="n_clicks")], [State("input-group-button-input", "value")])
def getAssetTimeline(n_clicks, userID):
    userID = userID.strip()       
    if n_clicks != 0:
        try:
            divs = getAssetDates(userID)
            assetTimeline = html.Div(
                children=divs
            )
            return assetTimeline
        except Exception as e:
            return [html.Br(), html.P("Please enter Valid Asset ID", style={'color': 'red'})]


@app.callback(Output("output-panel", "children"), [Input(component_id="input-group-button", component_property="n_clicks")], [State("input-group-button-input", "value")])
def getAssetInfo(n_clicks, userID):
    userID = userID.strip()       
    if n_clicks != 0:
        try:            
            name, symbol, cusip, description, country, currency, industry, location, exchange, active, earliestD, latestD = getAssetData(
                userID)
            act = 'A' if active else 'I'
            date = latestD.split(' ')

            age = datetime.fromisoformat(latestD).year - datetime.fromisoformat(earliestD).year 

            assetData = html.Div(
                [
                    # dbc.Row(
                    #     [
                    #         html.H6('Patient ID :'),
                    #         html.P(f'{id}')
                    #     ],
                    #     style={'text-align': 'center'}
                    # ),
                    # dbc.Row(
                    #     [
                    #         html.B('Sex :'),
                    #         html.P(f'{sex} '),
                    #         html.B('Age :'),
                    #         html.P(f'{age} '),
                    #         html.B('DOB :'),
                    #         html.P(f'{birthYear} '),
                    #         html.B('Deceased :'),
                    #         html.P(f'{dec}'),
                    #     ],
                    # ),
                    # dbc.Row(
                    #     [
                    #         html.B('Country :'),
                    #         html.P(f'{country} '),
                    #         html.B('Province :'),
                    #         html.P(f'{province} '),
                    #         html.B('City :'),
                    #         html.P(f'{city} '),
                    #     ],
                    # )

                    html.P(f'Asset ID: {userID}'),
                    html.P(
                        f'Asset Name: {name}'),
                    html.P(
                        f' Description: {description}'),
                    html.P(
                        f'Industry: {industry}'),
                    html.P(
                        f' Symbol: {symbol} Cusip: {cusip} Exchange: {exchange}'),
                    html.P(
                        f'Country: {country} Location: {location} Currency: {currency}'),
                    html.P(
                        f' Age: {age} DOB: {date[0]}'),
                ],
                style={'height': '100%', 'width': '100%',
                       'padding': '5px 0 0 0'},
            )
            return assetData
        except Exception as e:
            return [html.Br(), html.P("Please enter Valid Asset ID", style={'color': 'red'})]


def getAssetSubgraph(userID):
    
    userID = userID.strip()
            
    params = {"p": userID, "date1": "2014-01-15 00:00:00", "date2": "2015-01-15 00:00:00"}         
 
    q = conn.runInstalledQuery("getSubGraph", params)
    # print(q)
    nodes = []
    edges = []
    for data in q[0]['@@edgeSet']:
        nodes.append(
            {'data':
             {'id': data['from_id'], 'label': data['from_type']}
             }
        )
        nodes.append(
            {'data':
             {'id': data['to_id'], 'label': data['to_type']}
             }
        )
        edges.append(
            {'data':
             {'source': data['from_id'], 'target': data['to_id']}
             }
        )
    # elements = list(nodes) + list(edges)
    elements = nodes + edges
    return elements


@app.callback(Output("subgraph-div", "children"), [Input(component_id="input-group-button", component_property="n_clicks")], [State("input-group-button-input", "value")])
def assetSubgraph(n_clicks, userID):
    userID = userID.strip()   
    if n_clicks != 0:
        try:
            elements = getAssetSubgraph(userID)
            graph = cyto.Cytoscape(
                id='asset-subgraph',
                elements=elements,
                style={'width': '100%', 'height': '100%'},
                layout={
                    'name': 'cose'
                }
            )
            return graph
        except Exception as e:
            return [html.Br(), html.P("Error", style={'color': 'red'})]

def getAssetTimePrices(userID):
    userID = userID.strip()       
    q = conn.runInstalledQuery("get_asset_value", {'p': userID})

    try:
        x = np.array([q[0]["valueall"][i]["attributes"]["liquid_price"] for i in range(len(q[0]["valueall"]))])
        t = np.array([q[0]["valueall"][i]["attributes"]["sdate"] for i in range(len(q[0]["valueall"]))])

        i_sort = np.argsort(t)    

        df = pd.DataFrame(data=[[t[i_t].split(' ')[0],x[i_t]] for i_t in i_sort], columns=['Dates','Prices'])

    except Exception as e:
        print('error: ', e)
    return df

@app.callback(Output("price-time-div", "figure"), [Input(component_id="input-group-button", component_property="n_clicks")], [State("input-group-button-input", "value")])
def assetPriceGraph(n_clicks, userID):
    userID = userID.strip()   
    div = []
    fig = []
    if n_clicks != 0:
        try:
            df = getAssetTimePrices(userID)

#            fig = go.Figure(go.Scatter(x=df['Dates'], y=df['Prices']))

            fig = px.line(df, x='Dates', y='Prices')  
            
            return dcc.Graph(figure=fig)
        except Exception as e:
            return [html.Br(), html.P("Error", style={'color': 'red'})]


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]

global globalView
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return assetView
    elif pathname == "/page-2":
        return compositionView
    elif pathname == "/page-3":
        return mapView
    elif pathname == "/page-4":
        return dataView
    elif pathname == "/page-5":
        return aboutView

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    print("===================== STARTED =====================================")
    start_time = time.time()
    navbar , sidebar , assetView , compositionView , mapView  , dataView ,  aboutView = Setup_pages(conn,graphistry_un,graphistry_pw)
    content = html.Div(id="page-content", style=CONTENT_STYLE)
    app.layout = html.Div([dcc.Location(id="url"), navbar, sidebar, content])
    print("Fully loaded in ::   {}".format(str(timedelta(seconds=(time.time()-start_time)))))
    print("--------------------------------------------------------")
    app.run_server(port=8886)#, dev_tools_hot_reload=True)
    
    
    
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = px.data.stocks()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="ticker",
        options=[{"label": x, "value": x} 
                 for x in df.columns[1:]],
        value=df.columns[1],
        clearable=False,
    ),
    dcc.Graph(id="time-series-chart"),
])

@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("ticker", "value")])
def display_time_series(ticker):
    fig = px.line(df, x='date', y=ticker)
    return fig

app.run_server(port=8881)    
    
    
    
    
    
    
    

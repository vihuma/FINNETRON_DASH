import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import plotly.express as px



def get_page(conn):
    page = html.Div(
    [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                dbc.Row(
                                    dbc.InputGroup(
                                        [
                                            dbc.Input(
                                                id='input-group-button-input', placeholder='Enter Info', value="0000000"),
                                            dbc.InputGroupAddon(
                                                dbc.Button(
                                                    'Submit', id='input-group-button', n_clicks=0),
                                                addon_type='append'
                                            ),
                                        ],
                                    ),
                                    style={'width': '100%', 'height': '50px',
                                        'margin-bottom': '5px'},
                                ),
                                html.H3('Assset Information'),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            # html.Img(
                                            #     src='https://banner2.cleanpng.com/20180329/zue/kisspng-computer-icons-user-profile-person-5abd85306ff7f7.0592226715223698404586.jpg', height='150px'),
                                            html.Div(
                                                style={"background-color": "#424242", 'width': '100%', 'height': '100%'},
                                            ),
                                            width=3,
                                            # style={'padding-right': '10px'}
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                id='output-panel',
                                                style={"background-color": "#f8f9fa", 'width': '100%', 'height': '100%'},
                                            ),
                                            width=9,
                                            # style={'padding-left': '10px'}

                                        ),
                                    ],
                                    style={'width': '100%', 'height': '280px',
                                        'margin-bottom': '10px'}
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            # id='travel-counter-div',
                                            html.Div(
                                                id='vol-30-div',
                                                style={'text-align': 'center', 'vertical-align': 'middle',
                                                    'width': '100%', 'height': '100%', "background-color": "#f8f9fa",
                                                    'margin-right': '10px'},
                                            ),
                                            width=3,
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                id='vol-60-div',
                                                style={'text-align': 'center', 'vertical-align': 'middle',
                                                    'width': '100%', 'height': '100%', "background-color": "#f8f9fa",
                                                    'margin-right': '10px', 'margin-left': '10px'},
                                            ),
                                            width=3,
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                id='vol-180-div',
                                                style={'text-align': 'center', 'vertical-align': 'middle',
                                                    'width': '100%', 'height': '100%', "background-color": "#f8f9fa",
                                                    'margin-right': '10px', 'margin-left': '10px'},
                                            ),
                                            width=3,
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                id='vol-all-div',
                                                style={'text-align': 'center', 'vertical-align': 'middle',
                                                    'width': '100%', 'height': '100%', "background-color": "#f8f9fa",
                                                    'margin-left': '10px'},
                                            ),
                                            width=3,
                                        ),
                                    ],
                                    style={'width': '100%', 'height': '90px',
                                        'margin-bottom': '10px'}
                                ),
                            ],
                        ),
                        width=8,
                    ),
                    dbc.Col(
                        [
                            html.H3('Asset Timeline'),
                            html.Div(
                                id='timeline-div',
                            ),
                        ],
                        width=4,
                        style={'width': '100%', 'height': '470px',
                            "background-color": "#f8f9fa", "overflowY": "auto", "overflowX": "hidden", 'padding': '10px 10px 10px 20px'}
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3('Historical Prices'),                                                                        
                            html.Div(                            
                                id='price-time-div',
                                style={"height": "100%", 'width': '100%', "background-color": "#f8f9fa"}
#                                dcc.Graph(id='price-time-div'),
                            ),
                        ],
                        width=6,
                        style={'width': '100%', 'margin_right': '10px',
                               "background-color": "#f8f9fa", "overflowY": "auto", "overflowX": "hidden", 'padding': '10px 10px 10px 20px'}
                    ),
                    dbc.Col(
                        [
                            html.H3('Historical Returns'),                                                                                                    
                            html.Div(
                                id='return-time-div',
                                style={"height": "100%", 'width': '100%', "background-color": "#f8f9fa"},
#                                dcc.Graph(id='return-time-div'),
                            ),
                        ],
                        width=6,
                        style={'width': '100%', 'margin_left': '10px',
                               "background-color": "#f8f9fa", "overflowY": "auto", "overflowX": "hidden", 'padding': '10px 10px 10px 20px'}
                    ),
                ],
                style={'width': '100%', 'margin_top': '10px', 'height': '650px','margin_bottom': '10x',
                       "background-color": "#f8f9fa", "overflowY": "auto", "overflowX": "hidden", 'padding': '10px 10px 10px 20px'}                
            ),
            dbc.Row(
                [
                    html.H3('Value Graph'),                                                        
                    html.Div(
                        id='subgraph-div',
                        style={"height": "100%", 'width': '100%', "background-color": "#f8f9fa"},
                    ),
                ],
                style={'width': '100%', 'margin_top': '10px', 'height': '650px','margin_bottom': '10x',
                       "background-color": "#f8f9fa", "overflowY": "auto", "overflowX": "hidden", 'padding': '10px 10px 10px 20px'}
            ),
        ]
    )

    return page

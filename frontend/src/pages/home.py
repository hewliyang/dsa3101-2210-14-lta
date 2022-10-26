import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output

dash.register_page(__name__, path = '/')

layout = html.Div(children=[
    html.P("This is an application to calculate the density and probability of traffic jam on the road.", style={'padding':0, 'margin':0}),
    html.P("Jam Tracker consists of two pages, the map and the grid.", style={'padding':0, 'margin':0}),
    dcc.Tabs(id="tabs-about", value='model', children=[
        dcc.Tab(label='Model', value='model'),
        dcc.Tab(label='Map', value='map'),
        dcc.Tab(label='Grid', value='grid'),
    ]),
    html.Div(id='tabs-content', style={'max-height':'80vh'}),
    html.Footer('the application will be refreshed after predictions for all cameras have been made.', style={'padding':'2px 2px'})
], style={'max-height':'90vh'})

@callback(Output('tabs-content', 'children'),
              Input('tabs-about', 'value'))
def render_content(tab):
    if tab == 'model':
        return html.Div(
            [
                dbc.Row([
                    dbc.Col(
                        [
                            html.Div(
                                children = [
                                    html.H1('Model'),
                                    html.P('We used a pre-trained YOLO V4 model to count the number of vehicles that can be seen from\
										the cameras (Refer to the blue squares in the sample picture on the right). Next we perform a\
										calculation of the density by accounting for the number of vehicles per lane which we then use\
										to make a prediction on the probability of traffic jam for that direction')
                                ])
                        ], width = 6
                    ),
                    dbc.Col(
                        [
                            html.Img(src= '../assets/about_model.png', style={'height':'100%', 'width':'100%', 'max-height':'80vh', 'padding':'10px'})
                        ], width = 6
                    )
                ])
            ]
        )
    elif tab == 'map':
        return html.Div(
            [
                dbc.Row([
                    dbc.Col(
                        [
                            html.Div(
                                children = [
                                    html.H1('Map'),
                                    html.P('This page consists of a Singapore map with colour-coded markers on the location of all 87 cameras. The red markers represents\
                                    the location with high probability of traffic jam, followed by orange and green. Clicking on the markers will display the image\
                                    captured by the cameras, as well as the density and probability of traffic jam on each direction.')
                                    ]
                                )
                        ], width = 6
                    ),
                    dbc.Col(
                        [
                            dbc.Carousel(
                                items=[
                                    {"key": "1", "src": '../assets/about_map.png', "caption":"Overview"},
                                    {"key": "2", "src": '../assets/about_map_detailed.png', "caption":"Detailed"},
                                ],
                                ride = "carousel",
                                interval = 2000,
                                indicators=True,
                                variant = 'dark',
                                className="carousel-fade",
                                style={'height':'100%', 'width':'100%','max-height':'75vh', 'padding':'10px'}
                            )
                        ], width = 6
                    )
                ])
            #html.Img(src= '../assets/about_map.png',style={"width":"45%", "display":"inline-block"}),
            ]
        )
    else:
        return html.Div(
            [
                dbc.Row([
                    dbc.Col(
                        [
                            html.Div(
                                children = [
                                    html.H1('Grid'),
                                    html.P('This page displays the images captured by the cameras. The border of the images will be colour-coded just like the map.\
                                    Images are sorted by the probability of traffic jam at the locations in descending order. Clicking on the image will bring\
                                    you to a page displaying the density and probability of traffic jam for each direction, as well as the top 4 from the\
                                    remaining cameras with highest probability of traffic jam.')
                                ])
                        ], width = 6
                    ),
                    dbc.Col(
                        [
                            dbc.Carousel(
                                items=[
                                    {"key": "1", "src": '../assets/about_grid.png', "caption":"Overview"},
                                    {"key": "2", "src": '../assets/about_grid_detailed.png', "caption":"Detailed"},
                                ],
                                ride = "carousel",
                                interval = 2000,
                                indicators=True,
                                className="carousel-fade",
                                style={'height':'100%', 'width':'100%','max-height':'80vh', 'padding':'10px'}
                            )    
                        ], width = 6
                    )
                ])
            ]
        )
import dash
from dash import html, dcc

dash.register_page(__name__, path = '/')

Body = html.Div(children=[
    html.Br(),
    html.P("This is an application to calculate the density and probability of traffic jam on the road."),
    html.P("Jam Tracker consists of two pages, the map and the grid."),
    html.Br(),
    html.Div(children = [
        html.H1('Map'),
        html.P('This page consists of a Singapore map with colour-coded markers on the location of all 87 cameras. The red markers represents\
        the location with high probability of traffic jam, followed by orange and green. Clicking on the markers will display the image\
            captured by the cameras, as well as the density and probability of traffic jam on each direction.')
    ],style={"width":"45%", "display":"inline-block","float":"left"}),
    html.Div(children = [
        html.H1('Grid'),
        html.P('This page displays the images captured by the cameras. The border of the images will be colour-coded just like the map.\
        Images are sorted by the probability of traffic jam at the locations in descending order. Clicking on the image will bring\
        you to a page displaying the density and probability of traffic jam for each direction, as well as the top 4 from the\
        remaining cameras with highest probability of traffic jam.')
    ],style={"width":"45%", "display":"inline-block"}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Footer('the application will be refreshed after predictions for all cameras have been made.')
    
])

layout = html.Div(children=[
    # html.H1(children='This is our Home page'),
    # html.Div(children='This is our Home page content')
    Body
])

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output


dash.register_page(
    __name__,
    path='/gridDetailed',
    title='Grid Detailed View'
)


def create_card(img_src):
    return dbc.Card(
        [
            dbc.CardImg(src=img_src),
            dbc.Button("LayoutChange", color="primary"),
            dbc.CardLink("Clickme", href="#")
        ]
    )


def update_images(imgSrcList, clickedIndex):
    imgToDisplay = [imgSrcList[clickedIndex]]
    for i in range(len(imgSrcList)):
        if i != clickedIndex:
            imgToDisplay += [imgSrcList[i]]
        if len(imgToDisplay) == 5:
            break
    return imgToDisplay

# TODOs: Callbacks for list of images and page number
# img_main, img_b1, img_b2, img_b3, img_b4 = update_images(imgSrcList, clickedIndex)
# TODOs: Color borders based on traffic jam probability


layout = html.Div(
    [
        # First Row of Traffic Images
        # TODOs: Enhanced the size of this row
        dbc.Row(
            [
                dbc.Col(
                    [html.P("Placeholder", style={'textAlign': 'center', 'background-color': 'green', 'height': '60vh'}),
                     dbc.Button(href="http://127.0.0.1:8050/grid", style={'opacity':0})],
                    # [create_card(f'{img_main}')],
                    width=6
                ),
                dbc.Col(
                    html.P("Detailed Data on Current Image", style={
                        'textAlign': 'center', 'background-color': 'Yellow', 'height': '60vh'}),
                    width=6
                )
            ],
            className="g-0"
        ),
        # Next Top 4 Traffic Images
        dbc.Row(
            [
                dbc.Col(
                    html.P("Placeholder", style={
                        'textAlign': 'center', 'height': '20vh'}),
                    # [create_card(f'{img_b1}')],
                    width=3
                ),
                dbc.Col(
                    html.P("Placeholder", style={
                        'textAlign': 'center', 'height': '20vh'}),
                    # [create_card(f'{img_b2}')],
                    width=3
                ),
                dbc.Col(
                    html.P("Placeholder", style={
                        'textAlign': 'center', 'height': '20vh'}),
                    # [create_card(f'{img_b3}')],
                    width=3
                ),
                dbc.Col(
                    html.P("Placeholder", style={
                        'textAlign': 'center', 'height': '20vh'}),
                    # [create_card(f'{img_b4}')],
                    width=3
                )
            ],
            className="g-0"
        )
    ]
)

import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html, callback

jam = "https://i.ibb.co/xhwnPXB/JAM-01.png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=jam, height="30px")),
                        dbc.Col(dbc.NavbarBrand("JAM TRACKER", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="4F6D7A",
)
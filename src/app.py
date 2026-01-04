import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, html, dcc, callback, page_container
from dash.dependencies import Input, Output, State


def main():
    app = Dash(__name__, use_pages=False, external_stylesheets=[dbc.themes.MINTY, dbc.icons.BOOTSTRAP])
    app.title = "Fashionable"

    weather = "partly-cloudy"
    source = f"/assets/images/{weather}.png"

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="Fashionable",
        # brand_href="#",
        color="primary",
        dark=True,
    )

    card = dbc.Card(
            [
                html.Span(
                    [
                        html.H4("Weather", className="subtitle"), 
                        html.Span(
                            [
                                html.H5("°C"), 
                                daq.ToggleSwitch(id="temp-format", value=False), 
                                html.H5("°F")
                            ], className="switch"
                        )
                    ], className="card-header",
                ),
            dbc.CardImg(src=source, top=True, id="weather-image"),
            dbc.CardBody(
                [
                    html.H1("0°", id="temperature", className="card-title"),
                    html.H5("Lahti, Finland", id="location")
                ]
            ),
        ],style={"width": "20rem"})

    cardHat = dbc.Card(
            [
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src="/assets/images/hat.png", className="clothes-image"),
                    ]),
                    dbc.Col([
                        html.H5("Brown Flatcap"),
                    ]),
                ])
            ], className="card-clothes")
    cardJacket = dbc.Card(
            [
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src="/assets/images/jacket.png", className="clothes-image"),
                    ]),
                    dbc.Col([
                        html.H5("Navy Blue Overcoat"),
                    ]),
                ])
            ], className="card-clothes")
    cardShirt = dbc.Card(
            [
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src="/assets/images/shirt.png", className="clothes-image"),
                    ]),
                    dbc.Col([
                        html.H5("White Dress Shirt"),
                    ]),
                ])
            ], className="card-clothes")
    cardPants = dbc.Card(
            [
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src="/assets/images/pants.png", className="clothes-image"),
                    ]),
                    dbc.Col([
                        html.H5("Dark Blue Dress Pants"),
                    ]),
                ])
            ], className="card-clothes")
    cardShoes = dbc.Card(
            [
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src="/assets/images/shoes.png", className="clothes-image"),
                    ]),
                    dbc.Col([
                        html.H5("Dark Brown Oxford Shoes"),
                    ]),
                ])
            ], className="card-clothes")


    app.layout = html.Div([
            navbar,
            dbc.Row([
                dbc.Col(card, width=4),
                dbc.Col([
                    dbc.Row([cardHat]),
                    dbc.Row([cardShirt, cardJacket]),
                    dbc.Row([cardPants]),
                    dbc.Row([cardShoes]),
                    # dbc.Row([cardHat, cardJacket, cardShirt, cardPants, cardShoes])
                ], width=8),
            ]),
        ])
    return app.server

if __name__ == "__main__":
    app = main()
    # app.run_server(debug=True)
    app.run(debug=False)

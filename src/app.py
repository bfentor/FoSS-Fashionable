import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, html, dcc, callback, page_container, no_update
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv
import os
import weatherapi
from weatherapi.rest import ApiException
from src.fashionista import get_callback
import pandas as pd
# import requests
# from PIL import Image
# from dash_dynamic_images import image_callback

load_dotenv()

configuration = weatherapi.Configuration()
configuration.api_key['key'] = os.getenv('WEATHERAPI_KEY')

api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

def main():
    app = Dash(__name__, use_pages=False, external_stylesheets=[dbc.themes.MINTY, dbc.icons.BOOTSTRAP])
    app.title = "Fashionable"

    navbar = dbc.NavbarSimple(
        children=[
            # dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
            # dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="Fashionable",
        # brand_href="#",
        expand=False,
        sticky="top",
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
                                daq.ToggleSwitch(id="temp-format", value=False, persistence=True, persistence_type="local"), 
                                html.H5("°F")
                            ], className="switch"
                        )
                    ], className="card-header",
                ),
            dbc.CardImg(src=f"assets/images/weather/day/119.png", top=True, id="weather-image"),
            dbc.CardBody(
                [
                    html.H1("_", id="temperature", className="card-title"),
                    html.H5("This app requires location services to be enabled", id="prec-chance", className="weather"),
                    html.H2("______________", id="text", className="weather"),
                    html.H5("____, ____", id="location", className="weather"),
                ]
            ),
        ],style={"width": "20rem"}, id="weather-card")

    cardHead = dbc.Card(
            [
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src="/assets/images/head.png", className="clothes-image"),
                    ]),
                    dbc.Col([
                        html.H5("", id="head"),
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
                        html.H5("", id="jacket"),
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
                        html.H5("", id="shirt"),
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
                        html.H5("", id="pants"),
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
                        html.H5("", id="shoes"),
                    ]),
                ])
            ], className="card-clothes")


    app.layout = html.Div([
        navbar,
        dbc.Row([
            dbc.Col([
                card,
                dcc.Dropdown(["Unisex", "Female", "Male"], "Unisex", clearable=False, id="gender", placeholder="Gender", persistence=True, persistence_type="local"),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Refresh Location", id="location-perm-btn")
                    ], className="button-row"),
                    dbc.Col([
                        dbc.Button("Refresh Outfit", id="outfit-refresh-btn")
                    ], className="button-row")
                ], className="button-row")
        ]),
            dbc.Col([
                dbc.Row([cardHead], className="fit-row"),
                dbc.Row([cardShirt], className="fit-row"),
                dbc.Row([cardJacket], className="fit-row"),
                dbc.Row([cardPants], className="fit-row"),
                dbc.Row([cardShoes], className="fit-row"),
            ]),
        ]),
        dcc.Geolocation(id="geolocation"),
        dcc.Store(id="weatherapi-data", storage_type="session", data="dict"),
        dcc.Store(id="fit-store", storage_type="session", data="dict"),
    ])

    @callback(Output("geolocation", "update_now"), Input("location-perm-btn", "n_clicks"))
    def update_now(click):
        return True if click and click > 0 else False

    @callback(
        Output("weatherapi-data", "data"),
        Input("geolocation", "position"),
    )
    def populate_data(pos):
        if pos:
            q = f"{pos['lat']},{pos['lon']}"
            # return {"real_time": api_instance.realtime_weather(q), "forecast": api_instance.forecast_weather(q, 1)}
            return api_instance.forecast_weather(q, 1)
        return no_update

    @callback(
        Output("location", "children"),
        Output("temperature", "children"),
        Output("prec-chance", "children"),
        Output("weather-image", "src"),
        Output("text", "children"),
        Input("temp-format", "value"),
        Input("weatherapi-data", "data"),
        prevent_initial_callback=True,
    )
    def display_data(format, store):
        if store:
            # print(store)
            town = store['location']['name']
            country = store['location']['country']
            temp_string = "temp_f" if format else "temp_c"
            temp = store['current'][temp_string]
            img = store['current']['condition']['icon']
            
            text = store['current']['condition']['text']

            path = f"/assets/images/weather/{img[len(img)-11:]}"
            # print(f"PATH: {path}")
            
            rain = store['forecast']["forecastday"][0]["day"]["daily_chance_of_rain"]
            snow = store['forecast']["forecastday"][0]["day"]["daily_chance_of_snow"]
            chance = ""
            if (rain + snow) > 0:
                if rain > snow:
                    chance = f"Chance of rain: {rain}%"
                else:
                    chance = f"Chance of snow: {snow}%"

            return f"{town}, {country}", f"{round(temp)}°", chance, path, text
            
        return no_update, no_update, no_update, no_update, no_update

    @callback(
        Output("head", "children"),
        Output("shirt", "children"),
        Output("jacket", "children"),
        Output("pants", "children"),
        Output("shoes", "children"),
        Input("fit-store", "data"),
        Input("gender", "value"),
        prevent_initial_call=True
    )
    def set_fit(fdata, gender):
        if fdata:
            return fdata[gender]["head"], fdata[gender]["shirt"], fdata[gender]["jacket"], fdata[gender]["pants"], fdata[gender]["shoes"] 
        
        return no_update

    # This should really be in a seperate file but it doesn't want to be in a seperate file
    # Who am I to argue
    @callback(
        Output("fit-store", "data"),
        Input("weatherapi-data", "data"),
        Input("outfit-refresh-btn", "n_clicks")
    )
    def get_fit(wdata, n_clicks):
        if wdata:
            temp = wdata["current"]["feelslike_c"]
            rain = wdata['forecast']["forecastday"][0]["day"]["daily_will_it_rain"]
            snow = wdata['forecast']["forecastday"][0]["day"]["daily_will_it_snow"]

            # filter out clothes based on precipitation

            data = pd.read_csv("src/assets/database/db.csv")
            
            if rain + snow > 1:
                data = data[data["precipitation"] == True]
            
            data = data[(data["max"] > temp) & (data["min"] < temp)]

            mdata = data[(data["gender"] == "male") | (data["gender"] == "unisex")]
            fdata = data[(data["gender"] == "female") | (data["gender"] == "unisex")]
            
            # There is definetly a nice way to generalize this but I haven't the time for such niceties at the moment
            return {
                "Male": {
                    "head": mdata[mdata["type"] == "headwear"].sample(n=1)["name"].squeeze(), 
                    "shirt": mdata[mdata["type"] == "top"].sample(n=1)["name"].squeeze(), 
                    "jacket": mdata[mdata["type"] == "jacket"].sample(n=1)["name"].squeeze(), 
                    "pants": mdata[mdata["type"] == "bottom"].sample(n=1)["name"].squeeze(), 
                    "shoes": mdata[mdata["type"] == "footwear"].sample(n=1)["name"].squeeze(),
                },
                "Female": {
                    "head": fdata[fdata["type"] == "headwear"].sample(n=1)["name"].squeeze(), 
                    "shirt": fdata[fdata["type"] == "top"].sample(n=1)["name"].squeeze(), 
                    "jacket": fdata[fdata["type"] == "jacket"].sample(n=1)["name"].squeeze(), 
                    "pants": fdata[fdata["type"] == "bottom"].sample(n=1)["name"].squeeze(), 
                    "shoes": fdata[fdata["type"] == "footwear"].sample(n=1)["name"].squeeze(),
                },
                "Unisex": {
                    "head": data[data["type"] == "headwear"].sample(n=1)["name"].squeeze(), 
                    "shirt": data[data["type"] == "top"].sample(n=1)["name"].squeeze(), 
                    "jacket": data[data["type"] == "jacket"].sample(n=1)["name"].squeeze(), 
                    "pants": data[data["type"] == "bottom"].sample(n=1)["name"].squeeze(), 
                    "shoes": data[data["type"] == "footwear"].sample(n=1)["name"].squeeze(),
                }
            }
                    
        return no_update
    
    return app.server

if __name__ == "__main__":
    app = main()
    # get_callback(app)
    app.run(debug=False)

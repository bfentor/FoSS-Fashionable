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
import requests
import traceback

load_dotenv()

configuration = weatherapi.Configuration()
configuration.api_key['key'] = os.getenv('WEATHERAPI_KEY')

api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

def download_image(url, save_as):
    response = requests.get(url)
    with open(save_as, 'wb') as file:
        file.write(response.content)

def main():
    app = Dash(__name__, use_pages=False, external_stylesheets=[dbc.themes.MINTY, dbc.icons.BOOTSTRAP])
    app.title = "Fashionable"

    navbar = dbc.NavbarSimple(
        children=[
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
                        html.H5("", id="headwear"),
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
                        html.H5("", id="top"),
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
                        html.H5("", id="bottom"),
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
                        html.H5("", id="footwear"),
                    ]),
                ])
            ], className="card-clothes")


    app.layout = html.Div([
        navbar,
        dbc.Row([
            dbc.Col([
                card,
                dcc.Dropdown(["Unisex", "Female", "Male"], "Unisex", clearable=False, id="gender", placeholder="Gender", persistence=True, persistence_type="local", searchable=False),
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

    @callback(Output("geolocation", "update_now"), Input("location-perm-btn", "n_clicks"), prevent_initial_callback=True)
    def update_now(click):
        return True if click and click > 0 else False

    @callback(
        Output("weatherapi-data", "data"),
        Input("geolocation", "position"),
        prevent_initial_callback=True
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
            town = store['location']['name']
            country = store['location']['country']
            temp_string = "temp_f" if format else "temp_c"
            temp = store['current'][temp_string]
            img = store['current']['condition']['icon']

            imgp = img.split("/")

            text = store['current']['condition']['text']

            imgpath = f"/assets/images/weather/{imgp[len(imgp)-2]}/{imgp[len(imgp)-1]}"
            split = img[2:].split("/")
            split[split.index("64x64")] = "128x128"
            getimgurl = f"https://{"/".join(split)}"

            if not os.path.isfile("src" + imgpath):
                try:
                    download_image(getimgurl, "src" + imgpath)    
                except:
                    print("New image download failed")
                print(f"Downloaded new image: {getimgurl} | {"src" + imgpath}")
            
            rain = store['forecast']["forecastday"][0]["day"]["daily_chance_of_rain"]
            snow = store['forecast']["forecastday"][0]["day"]["daily_chance_of_snow"]
            chance = ""
            if (rain + snow) > 0:
                if rain > snow:
                    chance = f"Chance of rain: {rain}%"
                else:
                    chance = f"Chance of snow: {snow}%"

            return f"{town}, {country}", f"{round(temp)}°", chance, imgpath, text
            
        return no_update, no_update, no_update, no_update, no_update

    @callback(
        Output("headwear", "children"),
        Output("top", "children"),
        Output("jacket", "children"),
        Output("bottom", "children"),
        Output("footwear", "children"),
        Input("fit-store", "data"),
        Input("gender", "value"),
        prevent_initial_call=True
    )
    def set_fit(fdata, gender):
        if fdata:
            parts = {"headwear": "", "top": "", "jacket": "", "bottom": "", "footwear": ""}

            for i in parts.keys():
                if fdata[gender][i]:
                    parts[i] = fdata[gender][i]        

            # return fdata[gender]["head"], fdata[gender]["shirt"], fdata[gender]["jacket"], fdata[gender]["pants"], fdata[gender]["shoes"] 
            return parts["headwear"], parts["top"], parts["jacket"], parts["bottom"], parts["footwear"] 
        
        return no_update

    # This should really be in a seperate file but it doesn't want to be in a seperate file
    # Who am I to argue
    @callback(
        Output("fit-store", "data"),
        Input("weatherapi-data", "data"),
        Input("outfit-refresh-btn", "n_clicks"),
        prevent_initial_callback=True,
    )
    def get_fit(wdata, n_clicks):
        if wdata:
            temp = wdata["current"]["temp_c"]
            rain = wdata['forecast']["forecastday"][0]["day"]["daily_will_it_rain"]
            snow = wdata['forecast']["forecastday"][0]["day"]["daily_will_it_snow"]

            # filter out clothes based on precipitation

            data = pd.read_csv("src/assets/database/db.csv")
            
            if rain + snow > 1:
                data = data[data["precipitation"] == True]
            
            data = data[(data["max"] > temp) & (data["min"] < temp)]

            mdata = data[(data["gender"] == "male") | (data["gender"] == "unisex")]
            fdata = data[(data["gender"] == "female") | (data["gender"] == "unisex")]
            
            tables = {"Male": mdata, "Female": fdata, "Unisex": data}

            genders = ["Male", "Female", "Unisex"]
            types = ["headwear", "top", "jacket", "bottom", "footwear"]

            rdict = {"Male": {}, "Female": {}, "Unisex": {}}

            for i in genders:
                for k in types:
                    try:
                        rdict[i][k] = tables[i][tables[i]["type"] == k].sample(n=1)["name"].squeeze()
                    except Exception as e:
                        print(traceback.format_exc())
                        rdict[i][k] = ""

            return rdict
        
            # Leaving this here as a cautionary tale

            # There is definetly a nice way to generalize this but I haven't the time for such niceties at the moment
            # return {
            #     "Male": {
            #         "head": mdata[mdata["type"] == "headwear"].sample(n=1)["name"].squeeze(), 
            #         "shirt": mdata[mdata["type"] == "top"].sample(n=1)["name"].squeeze(), 
            #         "jacket": mdata[mdata["type"] == "jacket"].sample(n=1)["name"].squeeze() if temp < 15 else "", 
            #         "pants": mdata[mdata["type"] == "bottom"].sample(n=1)["name"].squeeze(), 
            #         "shoes": mdata[mdata["type"] == "footwear"].sample(n=1)["name"].squeeze(),
            #     },
            #     "Female": {
            #         "head": fdata[fdata["type"] == "headwear"].sample(n=1)["name"].squeeze(), 
            #         "shirt": fdata[fdata["type"] == "top"].sample(n=1)["name"].squeeze(), 
            #         "jacket": fdata[fdata["type"] == "jacket"].sample(n=1)["name"].squeeze() if temp < 15 else "", 
            #         "pants": fdata[fdata["type"] == "bottom"].sample(n=1)["name"].squeeze(), 
            #         "shoes": fdata[fdata["type"] == "footwear"].sample(n=1)["name"].squeeze(),
            #     },
            #     "Unisex": {
            #         "head": data[data["type"] == "headwear"].sample(n=1)["name"].squeeze(), 
            #         "shirt": data[data["type"] == "top"].sample(n=1)["name"].squeeze(), 
            #         "jacket": data[data["type"] == "jacket"].sample(n=1)["name"].squeeze() if temp < 15 else "", 
            #         "pants": data[data["type"] == "bottom"].sample(n=1)["name"].squeeze(), 
            #         "shoes": data[data["type"] == "footwear"].sample(n=1)["name"].squeeze(),
            #     }
            # }
                    
        return no_update
    
    return app.server

if __name__ == "__main__":
    app = main()
    # get_callback(app)
    app.run(debug=False)

import pandas as pd
from dash import callback, Output, Input, no_update

def get_callback(app):
    @app.callback(
        Output("fit-store", "data"),
        Input("weatherapi-data", "data")
    )
    def get_fit(wdata):
        if wdata:
            print("THIS IS A TEST")
            return {
                "Male": {
                    "head": "Male", 
                    "shirt":"Dark Blue T-Shirt", 
                    "jacket": "White Suit", 
                    "pants": "Grey Jeans", 
                    "shoes": "Black Boots"
                },
                "Female": {
                    "head": "Female", 
                    "shirt":"Dark Blue T-Shirt", 
                    "jacket": "White Suit", 
                    "pants": "Grey Jeans", 
                    "shoes": "Black Boots"
                },
                "Unisex": {
                    "head": "Unisex", 
                    "shirt":"Dark Blue T-Shirt", 
                    "jacket": "White Suit", 
                    "pants": "Grey Jeans", 
                    "shoes": "Black Boots"
                }
            }
        return no_update
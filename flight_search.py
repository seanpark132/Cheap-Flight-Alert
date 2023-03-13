# This class uses a flight information API (Tequila API) to search for the cheapest ticket for each input destination
# from the Google sheet.

import requests
from datetime import date, timedelta
import os
from dotenv import load_dotenv

load_dotenv(".env.txt")
TEQ_API_KEY = os.getenv("teq_api_key")

class FlightSearch:

    def __init__(self, FROM_IATA):
        self.from_iata = FROM_IATA

    def tequila_search(self, sheet_info):
        search_endpoint = "https://api.tequila.kiwi.com/v2/search"
        search_header = {
            "apikey": TEQ_API_KEY
        }
        tomorrow = date.today() + timedelta(days=1)
        six_months_later = date.today() + timedelta(days=180)
        date_from = tomorrow.strftime("%d/%m/%Y")
        date_to = six_months_later.strftime("%d/%m/%Y")

        flight_info_list = []
        for row in sheet_info:
            search_params = {
                "fly_from": self.from_iata,
                "fly_to": row["iataCode"],
                "date_from": date_from,
                "date_to": date_to,
                "nights_in_dst_from": 3,
                "nights_in_dst_to": 20,
                "flight_type": "round",
                "limit": 1,
                "curr": "CAD",
                "ret_from_diff_city": False,
                "ret_to_diff_city": False,
                "max_stopovers": 1
            }

            response = requests.get(url=search_endpoint, headers=search_header, params=search_params)
            response.raise_for_status()
            data = response.json()["data"]

            # if there are flights to this location, add the flight info to the flight info list
            if len(data) != 0:
                cheapest_flight_info = data[0]
                flight_info_list.append(cheapest_flight_info)

        return flight_info_list

    def get_IATA_codes(self, sheet_info):
        location_endpoint = "https://api.tequila.kiwi.com/locations/query"
        location_header = {
            "apikey": TEQ_API_KEY
        }

        IATA_list = []
        for row in sheet_info:
            city = row["city"]
            location_params = {
                "term": city,
                "location_types": "city"
            }
            response = requests.get(url=location_endpoint, headers=location_header, params=location_params)
            response.raise_for_status()
            data = response.json()
            IATA_code = data["locations"][0]["code"]
            IATA_list.append(IATA_code)

        return IATA_list





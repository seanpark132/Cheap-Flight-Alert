# This class uses the Sheety API to get destination airport codes and historical low prices from a Google sheet
# "prices" tab here: https://docs.google.com/spreadsheets/d/18gWk_LtP0w55oYFlBYdfXEMrENx05OCX_-OA6X78TEk/edit?usp=sharing

import requests

class DataManager:

    def __init__(self):
        self.prices_endpoint = "https://api.sheety.co/cc97706b3b69c6b8b6fdc3b123fbebb6/cheapFlightFinderSheet/prices"
        self.users_endpoint = "https://api.sheety.co/cc97706b3b69c6b8b6fdc3b123fbebb6/cheapFlightFinderSheet/users"

    def get_destination_info(self):
        response = requests.get(url=self.prices_endpoint)
        response.raise_for_status()
        data = response.json()
        destination_data = data["prices"]
        return destination_data

    def put_IATA_codes(self, IATA_list):
        for row_num, code in enumerate(IATA_list, 2):
            put_endpoint = self.prices_endpoint + f"/{row_num}"
            sheety_put_json = {
                "price": {
                    "iataCode": code
                }
            }
            response = requests.put(url=put_endpoint, json=sheety_put_json)
            response.raise_for_status()


    def get_user_info(self):
        response = requests.get(url=self.users_endpoint)
        response.raise_for_status()
        data = response.json()
        user_data = data["users"]
        return user_data

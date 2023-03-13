from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

FROM_CITY = "YVR"

sheety = DataManager()
searcher = FlightSearch(FROM_CITY)
alerter = NotificationManager()

# Get destination info and user info from Google sheet
destination_info = sheety.get_destination_info()
user_info = sheety.get_user_info()

# if Airport Code (IATA) column is not filled in, search for the correct codes and put them into the Google sheet
if destination_info[-1]["iataCode"] == "":
    IATA_list = searcher.get_IATA_codes(destination_info)
    sheety.put_IATA_codes(IATA_list)
    destination_info = sheety.get_destination_info()

# Search for cheapest flights from FROM_CITY to each destination city in sheet_info and return a list of flight info
flight_info_list = searcher.tequila_search(destination_info)

# For each flight from the search, check if it's price is lower than the price cutoff from the Google sheet
# If the price is lower, send a text and email all signed-up users
for flight_info in flight_info_list:
    destination_code = flight_info["cityCodeTo"]
    price = flight_info["price"]
    from_city = flight_info["cityFrom"]
    from_airport = flight_info["flyFrom"]
    to_city = flight_info["cityTo"]
    to_airport = flight_info["flyTo"]
    from_date = flight_info["route"][0]["local_departure"][0:10]
    to_date = flight_info["route"][-1]["local_arrival"][0:10]
    flight_link = flight_info["deep_link"]

    full_text = f"Low price alert! Only ${price} to fly from {from_city}-{from_airport} to {to_city}-{to_airport}" \
                f" from {from_date} to {to_date}"
    for row in destination_info:
        if destination_code == row["iataCode"] and price < row["historicalLowPrice"]:
            alerter.send_emails(user_info, flight_link, full_text)

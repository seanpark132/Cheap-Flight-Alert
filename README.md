# Cheap-Flight-Finder
A program that emails users with cheap flight deals for a list of destination cities. 

First, the program will use a spreadsheet API (Sheety API) to get a list of flight destinations and their historical low prices from a Google sheet. 
<a href="https://docs.google.com/spreadsheets/d/18gWk_LtP0w55oYFlBYdfXEMrENx05OCX_-OA6X78TEk/edit?usp=sharing" target="_blank">Link</a> to the Google sheet (prices tab). 
If the "IATA Code" (airport code) column is not filled out, the program will find the correct code for the destination using an airport information API 
(Tequila Location API) and put it on the sheet.

For each destination in the Google sheet, flight data for the lowest priced ticket in the next 6 months is pulled from a flight search API (Tequila Search API). 
By default, the following parameters are used when searching for flights from the API:
* Minimum trip duration: 3 days
* Maximum trip duration: 20 days
* Flight Type: round trip
* Maximum layovers: 1

If the prices of these tickets are lower than the historical low prices from the Google sheet, the program wiill email all signed-up users with important flight 
information and a link to book the flight. Users can sign-up to be emailed by running "sign_up.py" and entering their name and email. Their names and emails are
stored in the "users" tab in the Google sheet. 

![Error loading image](images/cheap_flight_finder.PNG?raw=true "Example email")

Before running the program, a valid Tequila API key must be input in the .env.txt file (teq_api_key). 

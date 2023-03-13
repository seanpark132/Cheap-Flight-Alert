# Run this script to sign users up to be emailed by the Cheap Flight Finder
# User info is stored in a Google sheet in the "users" tab:
# https://docs.google.com/spreadsheets/d/18gWk_LtP0w55oYFlBYdfXEMrENx05OCX_-OA6X78TEk/edit?usp=sharing

import requests

sheety_endpoint = "https://api.sheety.co/cc97706b3b69c6b8b6fdc3b123fbebb6/cheapFlightFinderSheet/users"

print("Welcome to Sean's Flight Club. \nWe find the best deals and email you.")
signed_up = False

first_name = input("What is your first name?\n")
last_name = input("What is your last name?\n")

while not signed_up:
  email = input("What is your email?\n")
  email_confirm = input("Type your email again to confirm\n")
  if email == email_confirm:
    print("You're in the club!")
    signed_up = True
  else:
    print("Please make sure to enter the same email twice.\n")

params = {
  "user": {
    "firstName":  first_name,
    "lastName": last_name,
    "email": email
  }
}

response = requests.post(url=sheety_endpoint, json=params)
response.raise_for_status()
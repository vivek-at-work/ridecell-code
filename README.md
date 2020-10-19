# Parking Managment Service


We are building a street parking spot reservation service. Each parking spot is identified by its location (lat, lng). Users should be able to view street parking spots, reserve and pay for the parking spots or cancel their reservations.

This Repo serves as a REST API.

**Tech Stack**
1. Python 3.8
2. Django 3.1
3. Postgres 10 & Postgis
4. Django Rest Framework

**Current Features:**

 1. See available parking spots on a map
 2. Search for an address and find nearby parking spot. (input: lat, lng, radius in meters. Output -
    list of parking spots within the radius).
 3. Reserve a parking spot
 4. View existing reservations
 5. Cancel an existing reservation
 6. Show the user the cost of the reservation
 7. Unit tests available
 8. Automated tests  Available
 9. Require users to use phone numbers to sign up.
 10. Validate that the phone numbers are real.

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
 
**How to Run on Dev**
1. git clone this repository
2. cd ridecell-code
3. pipenv install
4. Make Environnement variable to satify settings  for DB
5. cd parkingmanagement
6. execute "python manage.py  runserver 8001" this will bring up the local development server on port 8001.

**How to Run Tests**
1. git clone this repository
2. cd ridecell-code
3. pipenv install
4. Make Envoirenement variable to satify settings  for DB
5. cd parkingmanagement
6. execute "python manage.py test parkings" this will  test the parkings app.
7. execute "python manage.py test users" this will test the users app.

**How to Run e2e**
1. git clone this repository
2. cd ridecell-code
3. pipenv install
4. Make Envoirenement variable to satify settings  for DB
5. execute "python runner.py" this will perform testing via all exposed rest end points.


import requests
from requests.auth import HTTPBasicAuth

USERNAME = '8657946755'
PASSWORD = 'Qwerty@1234'

def display_names(l):
    for spot in l:
        print(spot['code'])

def perform_signup():
    url = 'http://127.0.0.1:8001/api/v1/users/signup/'
    user_data = {'contact_number': USERNAME, 'password': PASSWORD}
    x = requests.post(url, data=user_data)
    print(x.text)

def get_parking_spots():
    url = 'http://127.0.0.1:8001/api/v1/parkings/'
    x = requests.get(url,  auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print('{0} results on earth'.format(len(x.json())))
    print(display_names(x.json()))


def get_parking_spots_in_radius(radius=500):
    url = 'http://127.0.0.1:8001/api/v1/parkings/?lat=18.567124&long=73.769539&radius={0}'.format(
        radius)
    x = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print('{1} results in {0} m radius'.format(radius, len(x.json())))
    print(display_names(x.json()))


perform_signup()
get_parking_spots()
get_parking_spots_in_radius()
get_parking_spots_in_radius(1000)
get_parking_spots_in_radius(50000)

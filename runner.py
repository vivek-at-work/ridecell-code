import datetime

import requests
from requests.auth import HTTPBasicAuth

USERNAME = '8657946755'
PASSWORD = 'Qwerty@1234'



def perform_sign_up():
    url = 'http://127.0.0.1:8001/api/v1/users/signup/'
    user_data = {'contact_number': USERNAME, 'password': PASSWORD}
    print(f'CREATING A NEW USER WITH USERNAME {USERNAME} AND PASSWORD {PASSWORD}')
    create_user_response = requests.post(url, data=user_data)
    print(create_user_response.json())

def get_parking_spots():
    url = 'http://127.0.0.1:8001/api/v1/parkings/'
    print(f'GETING ALL PARKING SPOTS ON EARTH WITHOUT FILTER')
    parking_spots = requests.get(url,  auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print('{0} parking spots found on earth'.format(len(parking_spots.json())))


def get_parking_spots_in_radius(radius=500):
    url = 'http://127.0.0.1:8001/api/v1/parkings/?lat=18.567124&long=73.769539&radius={0}'.format(
        radius)
    print(f'GETING ALL PARKING SPOTS IN RADIUS OF {radius}')
    parking_spots = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print('{1} results in {0} m radius'.format(radius, len(parking_spots.json())))


def book_parking_spot():
    url = 'http://127.0.0.1:8001/api/v1/parkings/'
    x = requests.get(url,  auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print('Performing Reservation for {0}'.format(x.json()[0]['code']))
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()+datetime.timedelta(minutes=10)
    payload = {
            'from_time': start_time,
            'valid_up_to': end_time,
    }
    booking_response = requests.post('{}{}/'.format(x.json()[0]['url'],'reserve'),
                                      data=payload,auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print('Reservation Done  for {0} with response {1}'.format(x.json()[0]['code'],booking_response))


def cancel_parking_spot_booking():
    url = 'http://127.0.0.1:8001/api/v1/bookings/'
    bookings = requests.get(url,  auth=HTTPBasicAuth(USERNAME, PASSWORD))
    for booking in bookings.json():
        x = requests.post('{}{}/'.format(booking['url'],'cancel'), auth=HTTPBasicAuth(USERNAME, PASSWORD))
        print(x.json())

if __name__ == '__main__':
    perform_sign_up()
    get_parking_spots()
    get_parking_spots_in_radius()
    get_parking_spots_in_radius(800)
    get_parking_spots_in_radius(1000)
    get_parking_spots_in_radius(50000)
    book_parking_spot()
    get_parking_spots()
    cancel_parking_spot_booking()
    get_parking_spots()

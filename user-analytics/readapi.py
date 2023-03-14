import json
import os
import requests
import time
from dotenv import load_dotenv

def request_token(client_id, client_secret, code):
    response = requests.post(url='https://www.strava.com/oauth/token',
                             data={'client_id': client_id,
                                   'client_secret': client_secret,
                                   'code': code,
                                   'grant_type': 'authorization_code'})
    return response

def refresh_token(client_id, client_secret, refresh_token):

    response = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                             data={'client_id': client_id,
                                   'client_secret': client_secret,
                                   'grant_type': 'refresh_token',
                                   'refresh_token': refresh_token})
    return response


def write_token(token):

    with open('strava_token.json', 'w') as outfile:
        json.dump(token, outfile)


def get_new_token():
    request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                f'&response_type=code&redirect_uri={redirect_uri}' \
                f'&approval_prompt=force' \
                f'&scope=profile:read_all,activity:read_all'

    print('')
    print('Click here:', request_url)
    print('Please authorize the app and copy&paste below the generated code!')
    print('')
    code = input('Insert the code from the url: ')

    token = request_token(client_id, client_secret, code)

    #Save json response as a variable
    strava_token = token.json()
    # Save tokens to file
    write_token(strava_token)


def get_token():

    if not os.path.exists('./strava_token.json'):
        get_new_token()
    with open('strava_token.json', 'r') as token:
        data = json.load(token)

    return data


def save_activities(activities):
    with open('./user-analytics/data/activities.json', 'w') as output:
        json.dump(activities, output)


## MAIN SCRIPTS ##

load_dotenv()

client_id = os.environ.get("CLIENT_ID_2")
client_secret = os.environ.get("CLIENT_SECRET_2")
redirect_uri = 'http://localhost/'
n_activities = 200

data = get_token()

if data['expires_at'] < time.time():
    print('Refreshing token!')
    new_token = refresh_token(client_id, client_secret, data['refresh_token'])
    strava_token = new_token.json()
    # Update the file
    write_token(strava_token)

data = get_token()

access_token = data['access_token']

athlete_url = f"https://www.strava.com/api/v3/athlete?" \
              f"access_token={access_token}"
response = requests.get(athlete_url)
athlete = response.json()
if False:
    print('RESTful API:', athlete_url)
    print('='* 5, 'ATHLETE INFO', '=' * 5)
    print('Name:', athlete['firstname'],
        '"' + athlete['username'] + '"', athlete['lastname'])
    print('Gender:', athlete['sex'])
    print('City:', athlete['city'], athlete['country'])
    print('Strava athlete from:', athlete['created_at'])

activities_url1 = f"https://www.strava.com/api/v3/athlete/activities?" \
          f"access_token={access_token}" \
          f"&per_page={n_activities}&page=1"

response1 = requests.get(activities_url1)#, headers=header, params={'per_page':200, 'page':1})
print('Number of Activities Retrieved =', len(response1.json()))
if len(response1.json()) == 2:
    print('ERROR in API CALL:')
    print(response1.json())
    print('')
print('-------------------------')

save_activities(response1.json())

if False:
    activity = response.json()[5]

    print('='*5, 'SINGLE ACTIVITY', '='*5)
    print('Athlete:', athlete['firstname'], athlete['lastname'])
    print('Name:', activity['name'])
    print('Date:', activity['start_date'])
    print('Disance:', activity['distance'], 'm')
    print('Average Speed:', activity['average_speed'], 'm/s')
    print('Max speed:', activity['max_speed'], 'm/s')
    print('Moving time:', round(activity['moving_time'] / 60, 2), 'minutes')
    print('Location:', activity['location_city'], 
        activity['location_state'], activity['location_country'])
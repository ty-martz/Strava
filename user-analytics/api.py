import requests
import pandas as pd

access_token_1 = "user 1 token"
access_token_2 = "<user 2 access token>"

def get_user_activities(access_token):
    """
    Retrieves a list of activities from the Strava API for a given user and returns them as a pandas dataframe.
    """
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": "Bearer " + access_token}
    params = {"per_page": 200}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    # Get user 1 activities
    user_1_activities = get_user_activities(access_token_1)
    print(user_1_activities.head())
    user_1_activities.to_csv('user_1_activities.csv', index=False)

    # Get user 2 activities
    #user_2_activities = get_user_activities(access_token_2)
    #user_2_activities.to_csv('user_2_activities.csv', index=False)

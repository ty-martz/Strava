import pandas as pd
import json
import os
print(os.getcwd())

def preprocess_data(df):
    df = df[['Activity ID', 'Activity Date', 'Activity Name', 'Activity Type', 'Elapsed Time',
           'Elapsed Time.1', 'Distance', 'Distance.1', 'Max Heart Rate', 'Relative Effort',
           'Moving Time', 'Max Speed', 'Average Speed', 'Elevation Gain',
           'Elevation Loss', 'Elevation Low', 'Elevation High', 'Max Grade', 'Average Grade',
           'Average Heart Rate', 'Calories']]
    df.columns = [i.lower().replace(' ', '_') for i in df.columns]
    df['time_of_day'] = [i.split(',')[2].strip() for i in df['activity_date']]
    df['distance_m'] = df['distance.1'] / 1.609
    df['time_minutes'] = df['elapsed_time'] / 60
    df['max_speed_mph'] = df['max_speed'] * 2.237
    df['average_speed_mph'] = df['average_speed'] * 2.237
    df = df.rename(columns={'distance.1':'distance_km', 'elapsed_time.1':'time_sec'})

    return df

def col_val_counts(df, col):
    return df[col].value_counts()

def jsonify_counts(df):
    js = df.to_json()
    return js

if __name__ == '__main__':
    data = pd.read_csv('StravaDash/data/activities.csv')
    d = preprocess_data(data)
    active_counts_table = col_val_counts(d, 'activity_type')
    print(active_counts_table)
    json_data = jsonify_counts(active_counts_table)
    print('json =', json_data)

    with open('StravaDash/aggData/active_cnt.json', 'w') as outfile:
        json.dump(json_data, outfile)

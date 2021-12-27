import pandas as pd

data = pd.read_csv('StravaDash/data/activities.csv')

def preprocess_activities(df0):
    df0.columns = [i.lower().replace(' ', '_') for i in df0.columns]
    
    df = df0.copy()
    df['date_time'] = pd.to_datetime(df['activity_date']) - pd.Timedelta(hours=4)
    df['hour_of_day'] = df['date_time'].dt.hour
    df['month_of_year'] = df['date_time'].dt.month
    df['distance_miles'] = df['distance'] / 1.609
    df['time_minutes'] = df['elapsed_time'] / 60
    df['max_speed_mph'] = df['max_speed'] * 2.237
    df['average_speed_mph'] = df['average_speed'] * 2.237
    df['elevation_gain_ft'] = df['elevation_gain'] * 3.28084

    df = df.rename(columns={'distance':'distance_km', 'elapsed_time.1':'time_sec'})

    cols_to_keep = ['activity_id', 'date_time', 'activity_name', 'activity_type',
                'time_sec', 'distance_km', 'max_heart_rate', 'max_speed',
                'average_speed', 'elevation_gain', 'average_heart_rate',
                'calories', 'date_time', 'hour_of_day', 'month_of_year',
                'distance_miles', 'time_minutes', 'max_speed_mph', 'average_speed_mph',
                'elevation_gain_ft']
    return df[cols_to_keep]

out = preprocess_activities(data)
print(out.columns)
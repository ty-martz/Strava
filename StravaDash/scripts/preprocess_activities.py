import pandas as pd
import json

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


def get_activity_dataframes(df):
    '''
    Takes a dataframe of activities data and outputs a dictionary of dataframes filtered to activity type
    The activity type is the key and the filtered df is the value in the output dictionary
    '''
    activity_dfs = {}
    for a in df['activity_type'].unique():
        filt = df[df['activity_type'] == a]
        activity_dfs[a] = filt

    return activity_dfs


def get_run_stats(runs):
    '''
    Takes a df of running data and outputs a dictionary of different statistics
    '''
    run_dist_total_miles = sum(runs['distance_miles']) # recalc distance m
    run_speed_avg_mph = runs['average_speed_mph'].mean()
    run_count = len(runs) # calendar icon, animate filling up square behind it to reach %
    run_total_elevation = sum(runs['elevation_gain'].dropna()) # confirm measure
    run_hr_avg = runs['average_heart_rate'].mean()
    run_hr_max = max(runs['max_heart_rate'].dropna())
    run_cals_total = sum(runs['calories'].dropna()) # pizzas burned
    run_time_total = sum(runs['time_minutes'])

    stats = [run_dist_total_miles, run_speed_avg_mph, run_count, run_total_elevation, run_hr_avg,
             run_hr_max, run_cals_total, run_time_total]
    stat_names = ['total_miles', 'avg_speed', 'total_runs' 'total_elevation', 'avg_hr', 'max_hr',
                  'total_cals', 'total_time']
    d = {}
    for n, s in zip(stat_names, stats):
        d[n] = s
    return d


def col_val_counts(df, col='activity_type'):
    '''
    Runs value counts on a specified column of the input df
    '''
    return df[col].value_counts()


if __name__ == '__main__':
    data = pd.read_csv('StravaDash/data/activities.csv')
    out = preprocess_activities(data)
    activities_dict = get_activity_dataframes(out)
    running_stats = get_run_stats(activities_dict['Run'])
    with open('StravaDash/viz/run_stats.json', 'w') as outfile:
        json.dump(running_stats, outfile)

import pandas as pd

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
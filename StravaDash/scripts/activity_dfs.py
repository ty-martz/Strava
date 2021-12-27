import pandas as pd

def get_activity_dataframes(df):
    activity_dfs = {}

    for a in df['activity_type'].unique():
        filt = df[df['activity_type'] == a]
        activity_dfs[a] = filt

    return activity_dfs
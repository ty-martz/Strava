from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np
import clean_activities as pp
import json

app = Flask(__name__)

@app.route('/')
def index():
    data = pd.read_csv('../data/activities.csv')
    df = pp.preprocess_data(data)
    activity_cnt = pp.col_val_counts(df, 'activity_type')
    json_data = pp.jsonify_counts(activity_cnt)
    dd = {}
    for i in range(len(activity_cnt)):
        dd[activity_cnt.index.tolist()[i]] = activity_cnt.iloc[i]
    #dd = json.dumps(json_data)
    #dd = jsonify(activity_cnt)
    return render_template('index.html', data=dd)
    #return json_data

if __name__ == '__main__':
    app.run()

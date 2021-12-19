from flask import Flask, jsonify, render_template
import csv
import pandas as pd
import numpy as np
import scripts.clean_activities as pp

app = Flask(__name__)

@app.route('/')
def index():
    data = pd.read_csv('StravaDash/data/activities.csv')
    df = pp.preprocess_data(data)
    activity_cnt = pp.col_val_counts(df, 'activity_type')
    json_data = pp.jsonify_counts(activity_cnt)
    return render_template('templates/index.html', data=json_data)

if __name__ == '__main__':
    app.run()



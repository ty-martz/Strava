from flask import Flask, render_template
import pandas as pd
import clean_activities as pp
import os

print(os.getcwd())

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    data = pd.read_csv('StravaDash/data/activities.csv')
    df = pp.preprocess_data(data)
    activity_cnt = pp.col_val_counts(df, 'activity_type')
    dd = {}
    for i in range(len(activity_cnt)):
        dd[activity_cnt.index.tolist()[i]] = activity_cnt.iloc[i]
    return render_template('index.html', data=dd)


if __name__ == '__main__':
    app.run(debug=True)

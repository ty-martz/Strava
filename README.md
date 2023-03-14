# Strava Compare Dashboard

This Dashboard uses data compiled from the Strava V3 API and compares two users looking a few key metrics and comparisons based on the activities performed. The `user-analytics` folder is the key component holding the dash-plotly app and the required code.

[Click here](http://tymartz.pythonanywhere.com/) for a public version of the Dashboard and see it in action

## Usage

1. ```bash
git clone https://github.com/ty-martz/Strava.git

cd Strava

python -m venv env

source env/bin/activate 

pip install -r requirements.txt
```
This will provide the key files you need to make a comparison and then create an environment with the proper packages

2. Collect your Strava Data and the person you want to compare to.
    - If you get an export from Strava: Save the activities.csv files as u1_activities.csv and u2_activities.csv in the `data` folder
    - If you prefer to use the API, you will need to follow some different steps, continue below (note that this option will limit the number activities collected to 200 for each user)

3. To collect data from the API... COMING SOON

4. Once the files are saved with the proper names in the data folder, you can run the dash app
    - ```bash
    python app.py
    ```

5. Navigate to the specified local server, likely http://127.0.0.1:8050/ and see the comparison


## License

[MIT](https://choosealicense.com/licenses/mit/)
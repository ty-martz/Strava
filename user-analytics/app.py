import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Load the CSV datasets
df_user1 = pd.read_csv('./user-analytics/data/u1_activities.csv')
df_user2 = pd.read_csv('./user-analytics/data/u2_activities.csv')

# Load info
with open('./user-analytics/data/dash_info.txt', 'r') as file:
    msg = file.read()

# determine overlapping default range
if df_user2['start_date_local'].min() <= df_user1['start_date_local'].min():
    combo_start = df_user1['start_date_local'].min()
else:
    combo_start = df_user2['start_date_local'].min()
if df_user2['start_date_local'].max() >= df_user1['start_date_local'].max():
    combo_end = df_user1['start_date_local'].max()
else:
    combo_end = df_user2['start_date_local'].max()

# Define the color palette
colors = ['#fc5200', '#007FB6', '#6d6d78', '#36c597']

# Create the app
app = dash.Dash(__name__)
app.title = 'Strava Compare'
app._favicon = ("lightning32.png")

# Define the layout
app.layout = html.Div([
    ## TITLE ##
    html.Div([
        html.H1('Strava Compare', style={'color':colors[0], 'font-family':'sans-serif', 'display':'inline-block'}),
        html.Div([''], style={'width':'5%', 'display':'inline-block'}),
        html.A("Github Repo", href='https://github.com/ty-martz/Strava/tree/master/user-analytics', target="_blank", style={'display':'inline-block', 'color':colors[1]})
    ]),
    ## FILTERS ##
    html.Div([
        html.H2('Date Range:', style={'color':colors[1], 'font-family':'sans-serif'}),
        html.Div([
            dcc.DatePickerRange(
                id='date-range',
                start_date=combo_start,
                end_date=combo_end
            ),
        ], style={'display': 'inline-block'}),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.H2('Activity Type:', style={'color':colors[1], 'font-family':'sans-serif'}),
        html.Div([
            dcc.Dropdown(
                id='activity-dropdown',
                options=[{'label': i, 'value': i} for i in set(df_user1['type']).intersection(df_user2['type'])],
                value='Run'
            ),
        ], style={'display': 'inline-block', 'width':'80%'}),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.Div([msg], style={'padding':'2px 2px 2px 2px', 'font-family':'sans-serif', 'font-style':'italic', 'color':colors[2]}),
    ], style={'width':'25%', 'height':'900px', 'display': 'inline-block', 'verticalAlign': 'top', 'background-color': '#f2f2f2', 'top':'0', 'left':'0'}),
    ## VISUALS ##
    html.Div([
        html.Div([
            dcc.Graph(id='distance-graph'),
        ]),
        html.Div([
            html.Div([
                dcc.Graph(id='activity-counts'),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='elev-pie'),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),
    ], style={'width': '70%', 'display': 'inline-block', 'padding': '0 20'})
])

# Define the callback for the distance graph
@app.callback(
    Output('distance-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('activity-dropdown', 'value')
)
def update_distance_graph(start_date, end_date, activity_type):
    filtered_user1 = df_user1[(df_user1['start_date_local'] >= start_date) & (df_user1['start_date_local'] <= end_date) & (df_user1['type'] == activity_type)].sort_values('start_date_local').reset_index(drop=True)
    filtered_user2 = df_user2[(df_user2['start_date_local'] >= start_date) & (df_user2['start_date_local'] <= end_date) & (df_user2['type'] == activity_type)].sort_values('start_date_local').reset_index(drop=True)

    #filtered_user1 = filtered_user1.sort_values('start_date_local').reset_index(drop=True)
    #filtered_user2 = filtered_user2.sort_values('start_date_local', ascending=True).reset_index(drop=True)
    filtered_user1['rolling_dist'] = filtered_user1['distance'].cumsum()
    filtered_user2['rolling_dist'] = filtered_user2['distance'].cumsum()
    #print(filtered_user1[['start_date_local', 'rolling_dist']])

    fig = px.line(filtered_user1, x='start_date_local', y='rolling_dist', color_discrete_sequence=colors[0:1])
    fig.add_trace(px.line(filtered_user2, x='start_date_local', y='rolling_dist', color_discrete_sequence=colors[1:2]).data[0])

    fig.update_layout(
        title='Cumulative Distance',
        xaxis_title='Date',
        yaxis_title='Distance (meters)',
        #legend_title='User',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='left',
            x=1
        )
    )

    return fig

# Define the callback for the activity counts graph
@app.callback(
    Output('activity-counts', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('activity-dropdown', 'value')
)
def update_activity_counts(start_date, end_date, activity_type):
    filtered_user1 = df_user1[(df_user1['start_date_local'] >= start_date) & (df_user1['start_date_local'] <= end_date) & (df_user1['type'] == activity_type)]
    filtered_user2 = df_user2[(df_user2['start_date_local'] >= start_date) & (df_user2['start_date_local'] <= end_date) & (df_user2['type'] == activity_type)]

    counts_user1 = filtered_user1['type'].value_counts().sort_index()
    counts_user2 = filtered_user2['type'].value_counts().sort_index()

    fig = px.bar(
        pd.DataFrame({'User 1': counts_user1, 'User 2': counts_user2}).reset_index(),
        x='index', y=['User 1', 'User 2'], color_discrete_sequence=colors[0:2]
    )

    fig.update_layout(
        title='Activity Counts',
        xaxis_title='',
        yaxis_title='Count',
        legend_title='',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    return fig

# Define the callback for the elevation chart
@app.callback(
    Output('elev-pie', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('activity-dropdown', 'value')
)
def update_elev_pie(start_date, end_date, activity_type):
    filtered_user1 = df_user1[(df_user1['start_date_local'] >= start_date) & (df_user1['start_date_local'] <= end_date) & (df_user1['type'] == activity_type)]
    filtered_user2 = df_user2[(df_user2['start_date_local'] >= start_date) & (df_user2['start_date_local'] <= end_date) & (df_user2['type'] == activity_type)]

    elev_user1 = filtered_user1['total_elevation_gain'].sum()
    elev_user2 = filtered_user2['total_elevation_gain'].sum()

    fig = px.bar(
        pd.DataFrame({'User 1': elev_user1, 'User 2': elev_user2}, index=['User 1', 'User 2']).reset_index(),
        x='index', y=[elev_user1, elev_user2], color_discrete_sequence=colors[3:4]
    )

    fig.update_layout(
        title='Elevation Gained',
        xaxis_title='',
        yaxis_title='Elevation (m)',
        #legend_title='User'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


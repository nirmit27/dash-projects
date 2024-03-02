import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

adf = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                  encoding="ISO-8859-1",
                  dtype={'Div1Airport': str, 'Div1TailNum': str,
                         'Div2Airport': str, 'Div2TailNum': str})

data = adf.sample(n=500, random_state=42)

fig = px.pie(data, values='Flights', names='DistanceGroup',
             title='Distance group proportion by flights')

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Airline On-time Performance Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),
    html.P('Proportion of distance group (250 mile distance interval group) by flights.',
           style={'textAlign': 'center', 'color': '#F57241'}),
    dcc.Graph(figure=fig),
])

if __name__ == "__main__":
    app.run_server(debug=True)

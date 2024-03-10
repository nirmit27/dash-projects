import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, callback, Input, Output


data = pd.read_csv('/workspaces/dash-projects/data/historical_automobile_sales.csv')

year_list = [i for i in range(1980, 2024, 1)]

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]


app = Dash(__name__)

app.title = "Automobile Sales Statistics Dashboard"

app.layout = html.Div(children=[
    html.H1(children="Automobile Sales Statistics Dashboard", style={'fontSize': 24, 'textAlign':'center', 'color':'#503D36'}),
    
    html.Div([
        html.Label("Select Statistics :",),
        html.Br(),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            style={'textAlign': 'center', 'marginBlock': '0.75rem'}
        )
    ], style={'width': '80%', 'marginBlock': '2rem', 'marginInline':'auto'}),

    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year',
            style={'textAlign': 'center'}
        ), style={'width': '80%', 'marginBlock': '2rem', 'marginInline':'auto'}),

    html.Div([html.Div(id='output-container', className='chart-grid', style={'display':'flex'}),])

], style={'width':'80%', 'fontFamily': 'Cambria, sans-serif', 'marginInline':'auto'})


@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])

def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]


if __name__=="__main__":
    app.run(debug=True)
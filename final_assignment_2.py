import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, callback, Input, Output


year_list = [i for i in range(1980, 2024, 1)]
replace_types = {"Supperminicar": "Super Mini car", "Mediumfamilycar": "Medium Family car", "Smallfamiliycar": "Small Family car", "Sports": "Sports car", "Executivecar": "Executive car"}
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

df = pd.read_csv('/workspaces/dash-projects/data/historical_automobile_sales.csv')
df['Vehicle_Type'] = df['Vehicle_Type'].replace(replace_types)


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

    html.Div([html.Div(id='output-container', className='chart-grid',
                       style={'display':'flex', 'justifyContent':'center', 'alignItems':'center', }),])

], style={'width':'80%', 'fontFamily': 'Cambria, sans-serif', 'marginInline':'auto'})


@app.callback(
    Output(component_id='select-year', component_property='style'),
    Input(component_id='dropdown-statistics', component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])

def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = df[df['Recession'] == 1]
        
#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title='Average Automobile Sales over Recession Period',
                           labels={"Year": "Years", "Automobile_Sales": "Automobile Sales"},))

#Plot 2 Calculate the average number of vehicles sold by vehicle type
        
        yearly_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        R_chart2 = dcc.Graph(
            figure=px.bar(yearly_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Number of Vehicles sold by Vehicle Type",
                          labels={ "Vehicle_Type": "Vehicle Type", "Automobile_Sales": "Automobile Sales"}))
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        
        type_share = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(
            figure=px.pie(type_share, values=type_share['Advertising_Expenditure'], labels=type_share['Vehicle_Type'],
                         names=type_share['Vehicle_Type'], title='Total expenditure share by Vehicle Type during recessions'))

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        
        ue_rate = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(ue_rate, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
             labels={'Automobile_Sales': 'Average Automobile Sales', 'unemployment_rate': 'Unemployment Rate'},
             title='Effect of Unemployment Rate on Vehicle Type and Sales', barmode='group'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],)
        ]
    
    # 


if __name__=="__main__":
    app.run(debug=True)
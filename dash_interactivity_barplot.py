import pandas as pd

# PLOTLY
import plotly
import plotly.express as px
import plotly.graph_objects as go

# DASH
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# DATASET
adf = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', encoding = "ISO-8859-1", dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str})


# HTML
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Total number of flights to the destination state split by reporting airline', style={'textAlign':'center', 'color':'#503D36', 'font-size': 40}),
    html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number', style={'height':'50px', 'font-size': 35}),],
    style={'font-size': 40}),html.Br(),html.Br(),
    html.Div(dcc.Graph(id='bar-plot')),
])


# CALLBACK
@app.callback(Output(component_id='bar-plot', component_property='figure'), Input(component_id='input-year', component_property='value'))
def get_graph(entered_year):

    # DATA
    df = adf[adf['Year']==int(entered_year)]
    bdf = df.groupby('DestState')['Flights'].sum().reset_index()

    # PLOT
    fig = px.bar(bdf, x='DestState', y='Flights', title='Total number of flights to the destination state split by reporting airline')
    fig.update_layout(title='Flights to Destination State', xaxis_title='Destination state', yaxis_title='Flights')

    return fig

# DRIVER
if __name__=="__main__":
    app.run_server()
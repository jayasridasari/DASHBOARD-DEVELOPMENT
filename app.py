import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("/content/owid-covid-data.csv")
df = df[df['continent'].notna()]  # Filter out global aggregates

# Initialize app
app = dash.Dash(__name__)
app.title = "COVID-19 Dashboard"

# Layout
app.layout = html.Div([
    html.H1("🌍 COVID-19 Dashboard", style={"textAlign": "center"}),
    
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in df['location'].unique()],
            value='India'
        ),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=pd.to_datetime(df['date']).min(),
            max_date_allowed=pd.to_datetime(df['date']).max(),
            start_date='2021-01-01',
            end_date='2021-12-31'
        )
    ], style={'width': '80%', 'margin': 'auto'}),

    dcc.Graph(id='cases-line'),

    dcc.Graph(id='daily-bar'),
])

# Callbacks
@app.callback(
    [Output('cases-line', 'figure'),
     Output('daily-bar', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graphs(country, start, end):
    dff = df[(df['location'] == country) & 
             (df['date'] >= start) & (df['date'] <= end)]
    
    fig1 = px.line(dff, x='date', y='total_cases', title='Total Confirmed Cases')
    fig2 = px.bar(dff, x='date', y='new_cases', title='Daily New Cases')

    return fig1, fig2

# Run server
if __name__ == '__main__':
    app.run(debug=True)

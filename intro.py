import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from DHT11 import loop

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Starting the application.
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Importing and cleaning data to be used.


#Layout of the application (Dash components, HTML).
app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(
        className="temp",
        style={'width': '50%'},
        children=[
            dcc.Graph(id='live-update-graph-temp'),
            dcc.Graph(id='live-update-graph-humidity')
        ]),
])


# Multiple components can update everytime interval gets fired.
@app.callback(
        [Output('live-update-graph-temp', 'figure'),
         Output('live-update-graph-humidity','figure')],
        [Input('interval-component', 'n_intervals')])

def update_graph_live(n):

    # Collect some data
    data = loop()
    humidity = data[0]
    temperature = data[1]

    # Create the graph with subplots

    # Humidity Gauge
    humidityFig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=humidity,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Humidity"}))

    # Temperature Gauge
    temperatureFig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temperature,
                         #   gauge={'axis': {'range': [-2, 11]},
                        #'steps': [
                         #   {'range': [-2, 0], 'color': "white"},
                          #  {'range': [0, 7], 'color': "white"},
                           # {'range': [7, 11], 'color': "white"}],
                        #'threshold': {'line': {'color': "black", 'width': 1}, 'thickness': 1, 'value': 7}},
        # width=200,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Temperature"}))

    return temperatureFig,humidityFig

if __name__ == '__main__':
    app.run_server(debug=True)
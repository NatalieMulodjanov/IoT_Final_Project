import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from DHT11 import loop
from MQTTClient import subscribe
from led import setLED
from emailClient import sendEmail

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
    html.Div(
        className="light",
        style={'width': '50%'},
        children=[
            dcc.Graph(id='live-update-graph-light')
        ])
])


# Multiple components can update everytime interval gets fired.
@app.callback(
        [Output('live-update-graph-temp', 'figure'),
         Output('live-update-graph-humidity','figure'),
         Output('live-update-graph-light','figure')],
        [Input('interval-component', 'n_intervals')])

def update_graph_live(n):

    # Collect some data
    #data = loop()
    #humidity = data[0]
    #temperature = data[1]

    light = float(subscribe("light")) # Subscribing to the light topic

    # notifications or actions
    if (light < 400):
        setLED(True)
        sendEmail()
    else:
        setLED(False)



    # Create the graph with subplots

    # Humidity Gauge
    humidityFig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=10,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Humidity"}))

    # Temperature Gauge
    temperatureFig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=10,
                         #   gauge={'axis': {'range': [-2, 11]},
                        #'steps': [
                         #   {'range': [-2, 0], 'color': "white"},
                          #  {'range': [0, 7], 'color': "white"},
                           # {'range': [7, 11], 'color': "white"}],
                        #'threshold': {'line': {'color': "black", 'width': 1}, 'thickness': 1, 'value': 7}},
        # width=200,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Temperature"}))

    # Light Gauge
    lightFig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=light,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Light"}))


    return temperatureFig,humidityFig,lightFig



if __name__ == '__main__':
    app.run_server(debug=True)
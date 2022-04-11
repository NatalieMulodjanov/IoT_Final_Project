import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from DHT11 import loop
from MQTTClient import subscribe
from led import setLED
from emailClient import sendEmail

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Starting the application.
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets,dbc.themes.BOOTSTRAP])

#Importing and cleaning data to be used.


#Layout of the application (Dash components, HTML).
app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(
        className="temp",
        style={'width': '50%','border-style': 'solid'},
        children=[
            dcc.Graph(id='live-update-graph-temp'),
            dcc.Graph(id='live-update-graph-humidity')
        ]),
    html.Div(
        className="light",
        style={'width': '50%', 'border-style': 'solid'},
        children=[
            dcc.Graph(id='live-update-graph-light',style={'width':'50%','height':'50%'}),
            html.Img(id='led-status'),
            dbc.Toast([html.P("An email has been sent.")], id='light-notification', header='Light is under 400!', dismissable=True, is_open=False,style={'width':'50%','height':'25%','margin-top':'auto'})
        ])
])


# Multiple components can update everytime interval gets fired.
@app.callback(
        [Output('live-update-graph-temp', 'figure'),
         Output('live-update-graph-humidity','figure'),
         Output('live-update-graph-light','figure'),
         Output('led-status','src'),
         Output('light-notification','is_open')],
        [Input('interval-component', 'n_intervals')])

def update_graph_live(n):

    # Collect some data
    #data = loop()
    #humidity = data[0]
    #temperature = data[1]

    light = float(subscribe("light")) # Subscribing to the light topic


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


    # notifications or actions
    if (light < 400):
        light_notif = True
        src = 'data:image/png;base64,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'
        setLED(True)
        sendEmail()
    else:
        light_notif = False
        src = 'http://www.clker.com/cliparts/I/s/H/l/t/7/off-lightbulb-md.png'
        setLED(False)

    return temperatureFig,humidityFig,lightFig,src,light_notif



if __name__ == '__main__':
    app.run_server(debug=True)
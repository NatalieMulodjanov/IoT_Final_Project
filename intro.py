import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from DHT11 import loop
from MQTTClient import subscribe
from led import setLED
from emailClient import sendEmail, receive_email


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Starting the application.
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets,dbc.themes.BOOTSTRAP])

#Importing and cleaning data to be used.


#Layout of the application (Dash components, HTML).
app.layout = html.Div(children =[
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
        style={'width': '50%'},
        children=[
            dcc.Graph(id='live-update-graph-light'),
            html.Img(id='led-status'),
            dbc.Toast([html.P("An email has been sent.")], id='light-notification', header='Light is under 400!', dismissable=True, is_open=False,style={'width':'50%','height':'25%','margin-top':'auto'})
        ]),
    html.Div(
        className="fan",
        style={'width': '50%'},
        children=[
            html.Img(id='fan_status', style={'width': '100%'})
        ]),
])

emailSent = False
fanTurnedOn = False

# Multiple components can update everytime interval gets fired.
@app.callback(
        [Output('live-update-graph-temp', 'figure'),
         Output('live-update-graph-humidity','figure'),
         Output('live-update-graph-light','figure'),
         Output('led-status','src'),
         Output('light-notification','is_open'),
         Output('fan_status','src')],
        [Input('interval-component', 'n_intervals')])

def update_graph_live(n):

    # Collect temperature and humidity data via the RPI.
    #data = loop()
    #humidity = data[0]
    #temperature = data[1]

    light = float(subscribe("light")) # Subscribing to the light topic
    #humidity = float(subscribe("humidity"))
    #temp = float(subscribe("temperature"))

    humidity = 10
    temp = 10

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
        value=temp,
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

    # notifications or actions for the light.
    if (light < 400):
        light_notif = True
        led_src = '/assets/light_on.png'
        setLED(True)
        sendEmail("Light is at " + str(light) + "! Please turn on the lights!")
        print("LED Email sent")
    else:
        light_notif = False
        led_src = '/assets/light_off.png'
        setLED(False)


    # notifications or actions for the temperature.
    global emailSent
    if temp > 23:
        if emailSent == False:
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?")
            print("Temp Email sent")
            emailSent = True


    # notifications or actions for the temperature.
    global fan_src
    global fanTurnedOn
    # receivedEmail = receive_email()
    # print(receivedEmail["Content"])
    # if "YES" in receivedEmail["Content"]:
    #     # print("Turning on the fan")
    #     # fan_src='/assets/fan_on.jpg'
    #     fanTurnedOn = True
    #     # turnOnFan()

    # notifications or actions for the fan.
    if (fanTurnedOn == True):
        fan_src = '/assets/fan_on.jpg'
    else:
        fan_src = '/assets/fan_off.jpg'

    return temperatureFig,humidityFig,lightFig,led_src,light_notif,fan_src



if __name__ == '__main__':
    app.run_server(debug=True)
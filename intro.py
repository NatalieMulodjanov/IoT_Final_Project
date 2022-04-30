import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from DHT11 import loop
from MQTTClient import subscribe
from led import setLED
from emailClient import sendEmail, receive_email
from fan import turnOnFan
import connectionManager


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Starting the application.
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Importing and cleaning data to be used.



#fan picture for dashboard
srcImg = '/assets/fan_off.jpg'

#Layout of the application (Dash components, HTML).
app.layout = html.Div(children =[
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
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
        style={'width': '50%', "background": "black"},
        children=[
            dcc.Graph(id='live-update-graph-light')
        ]),
    html.Img(id='fan_status', src=srcImg ,style={'width': '100%'})
])

emailSent = False
fanTurnedOn = False


# Multiple components can update everytime interval gets fired.
@app.callback(
        [Output('live-update-graph-temp', 'figure'),
         Output('live-update-graph-humidity','figure'),
         Output('live-update-graph-light','figure')],
        [Input('interval-component', 'n_intervals')])

def update_graph_live(n):

    # Collect some data

    light = float(subscribe("light")) # Subscribing to the light topic
    humidity = float(subscribe("humidity"))
    temp = float(subscribe("temperature"))
    user_rfid = subscribe("user_rfid")
    user = connectionManager.getUser(user_rfid)
    sendEmail("User " + user[3] + " has connected")
    print(user)
    global emailSent
    if temp > user[1]:
        if emailSent == False:
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?")
            print("Email sent")
            emailSent = True
    
    print("Hum: ", humidity)
    print("Temp: ", temp)
    print("Light:", light)
    # notifications or actions
    if (light < user[2]):
        if emailSent == False:
            setLED(True)
            sendEmail("The Light is under 400! Turn on the lights please.")
            emailSent = True
    else:
        setLED(False)


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
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Temperature"}))

    # Light Gauge
    lightFig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=light,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Light"}))

    global src
    global fanTurnedOn
    receivedEmail = receive_email()
    print(receivedEmail["Content"])
    if "YES" in receivedEmail["Content"]:
        print("Turning on the fan")
        src='/assets/fan_on.jpg'
        fanTurnedOn = True
        turnOnFan()

    return temperatureFig,humidityFig,lightFig



if __name__ == '__main__':
    app.run_server(debug=True)
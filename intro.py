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

from DCMotor import startMotor

global tempEmailSent
global lightEmailSent
global led_src
global fan_src
global light_notif
global emailRequestSent

lightEmailSent = False
tempEmailSent = False
led_src = '/assets/light_off.png'
fan_src = '/assets/fan_off.png'
emailRequestSent = False
light_notif = False

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

    # ---------- Calling Global Variables ------
    global tempEmailSent
    global lightEmailSent
    global led_src
    global fan_src
    global light_notif
    global emailRequestSent

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

    #  --------- NOTIFICATIONS OR ACTIONS ------------

    # Checking temperature and light and performing actions based on constraints.
    if temp > user[1] and light < user[2]:
        led_src = '/assets/light_on.png' # Changing the LED image.
        light_notif = True # Send a notification that LED is on.
        if tempEmailSent == False: # If an email has not been sent yet.
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?") # Send temperature email.
            tempEmailSent = True # The email has been sent.
            emailRequestSent = True # Check for a response.
            print("Temperature email sent!") # CMD Line notification that emails have been sent.
        if lightEmailSent == False:
            sendEmail("The Light is under 400! Turn on the lights please.") # Send light email.
            lightEmailSent = True
            print("Light email sent!")
    elif temp > user[1]:
        light_notif = False # Don't send a LED notification.
        led_src = '/assets/light_off.png' # Changing the LED image.
        if tempEmailSent == False: # If an email has not been sent yet.
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?") # Sending temperature email.
            tempEmailSent = True # The email has been sent.
            emailRequestSent = True # Check for a response.
            print("Temperature Email Sent!") # CMD Line notification that an email has been sent.
    elif light < user[2]:
        light_notif = True # Send a LED notification.
        led_src = '/assets/light_on.png' # Change the LED image.
        if lightEmailSent == False: # If an email has not been sent yet.
            sendEmail("The Light is under 400! Turn on the lights please.") # Send light email.
            lightEmailSent = True # The email has been sent.
            emailRequestSent = False # We are not waiting for a response.
            print("Light Email Sent!") # CMD Line notification that an email has been sent.
    else:
        light_notif = False # No LED notification.
        lightEmailSent = False
        tempEmailSent = False
        emailRequestSent = False # We are not awaiting a response.
        led_src = '/assets/light_off.png' # Changing the LED image.
        fan_src = '/assets/fan_off.png' # Set the image to fan off.

    if emailRequestSent:
        print("Checking email for response.")
        if receive_email():
            print("Response: Yes")
            fan_src = '/assets/fan_on.png' # Change the image.
            startMotor() # Turn on the fan.
            print("The fan is turned on!") # CMD line notif.
            emailRequestSent = False
            tempEmailSent = False
            fanTurnedOn = True # The fan is on.
        else:
            print("No response.")
            fanTurnedOn = False # The fan is off.
            fan_src = '/assets/fan_off.png' # Set the image to fan off.


    if (light_notif):
        setLED() # Turning on the LED.

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
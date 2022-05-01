import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from DHT11 import loop
from MQTTClient import subscribe
from led import setLED
from emailClient import sendEmail, receive_email
from db import start,get
import connectionManager
from DCMotor import startMotor

global tempEmailSent
global lightEmailSent
global led_src
global fan_src
global light_notif
global emailRequestSent
global user
global isDatabaseSet
global username
global userTemp
global userHumidity
global userLight
global userImage
global temp
global humidity
global fanText
global fanTurnedOn

user = 'admin'
isDatabaseSet = False
lightEmailSent = False
tempEmailSent = False
led_src = '/assets/light_off.png'
fan_src = '/assets/fan_off.png'
emailRequestSent = False
light_notif = False
username = 'Admin'
userTemp = 26.0
userHumidity = 45.0
userLight = 350.0
userImage = '/assets/knight.png'
temp = 0.0
humidity = 0.0
fanText = "The fan is OFF!"
fanTurnedOn = False

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','/assets/stylesheet2.css']


# Starting the application.
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Layout of the application (Dash components, HTML).
app.layout = html.Div(children =[
    dcc.Interval(
        id='interval-component',
        interval=7*1000,  # in milliseconds
        n_intervals=0
    ),
    html.H1(style={'text-align':'center'},children=["IoT Home Dashboard"]),
    html.Br(),html.Br(),
    dbc.Toast([html.P("An email has been sent.")], id='light-notification', header='Light is under the threshold!', is_open=False,style={'text-align': 'center'}),
    html.Table(
        style={'width': '100%'},
        children=[
            html.Tr(
                children=[
                    html.Th(style={'text-align':'center'},children=['Temperature and Humidity']),
                    html.Th(style={'text-align':'center'},children=['Fan Status']),
                    html.Th(style={'text-align':'center'},children=['Light'])
                ]),
            html.Tr(
                children=[
                    html.Td(
                    style={'width':'33%','text-align': 'center'},
                    children=[
                        html.Br(),
                        html.H5("Current Temperature Threshold: 0.0", id='temp-threshold', style={'text-align': 'center', 'color':'red'}),
                        daq.Gauge(id='live-update-graph-temp', showCurrentValue=True, label='Temperature', max=50, min=0),
                        daq.Gauge(id='live-update-graph-humidity', showCurrentValue=True, label='Humidity',max=100, min=0),
                        html.Br()
                    ]),
                    html.Td(
                    style={'width':'33%','display': 'block','margin-left':'auto','margin-right':'auto'},
                    children=[
                        html.Br(),
                        html.H5("The fan is OFF!", id="fan-status-text", style={'text-align': 'center'}),
                        html.Img(id='fan_status', style={'width':'250px','height':'250px'}),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.P("User: Knight", id='user-name', style={'text-align': 'center'}),
                        html.Img(id='user-img', style={'width': '250px', 'height': '200px'})

                    ]),
                    html.Td(
                        style={'width':'33%','text-align': 'center'},
                        children=[
                            html.H5("Current Light Threshold: 0.0", id='light-threshold', style={'text-align': 'center','color':'red'}),
                            daq.Gauge(id='live-update-graph-light', showCurrentValue=True, label='Light',max=4000, min=0),
                            html.P('LED Status'),
                            html.Br(),
                            html.Img(id='led-status', style={'width': '250px','height': '250px'})
                    ])
            ])
        ])
    ])

# Multiple components can update everytime interval gets fired.
@app.callback(
        [Output('live-update-graph-temp', 'value'),
         Output('live-update-graph-humidity','value'),
         Output('live-update-graph-light','value'),
         Output('led-status','src'),
         Output('light-notification','is_open'),
         Output('fan_status','src'),
         Output('user-img','src'),
         Output('temp-threshold','children'),
         Output('user-name', 'children'),
         Output('light-threshold','children'),
         Output('fan-status-text','children')],
        [Input('interval-component', 'n_intervals')])

def update_graph_live(n):

    # ---------- Calling Global Variables ------
    global tempEmailSent
    global lightEmailSent
    global led_src
    global fan_src
    global light_notif
    global emailRequestSent
    global user
    global username
    global userTemp
    global userHumidity
    global userLight
    global userImage
    global isDatabaseSet
    global temp
    global humidity
    global fanTurnedOn
    global fanText

    # --------- DATA COLLECTION ----------------

    # Instantiating database data if it is the first time.
    if (isDatabaseSet == False):
        start()
        isDatabaseSet = True

    # Fetching the User via MQTT.
    user_rfid = str(subscribe("user_rfid"))
    user = get(user_rfid)

    # Sending the email that the user has connected.
    if(username != user[0]['name']):
        sendEmail("User " + user[0]['name'] + " has connected")
        print("New User Email Sent!")

    # Setting User information
    username = user[0]['name']
    userTemp = float(user[0]['temperature'])
    userHumidity = float(user[0]['humidity'])
    userLight = float(user[0]['light'])
    userImage = user[0]['image']

    # Fetching the light data via MQTT.
    light = float(subscribe("light")) # Subscribing to the light topic

    # Fetching the humidity and temp via RPI.
    data = loop()
    humidity = data[0]
    temp = data[1]

    # Printing the fetched values.
    print("User Name: " + user[0]['name'])
    print("Hum: ", humidity)
    print("Temp: ", temp)
    print("Light:", light)

    #  --------- NOTIFICATIONS OR ACTIONS ------------

    # Checking temperature and light and performing actions based on constraints.
    if temp > userTemp and light < userLight:
        led_src = '/assets/light_on.png' # Changing the LED image.
        light_notif = True # Send a notification that LED is on.
        if tempEmailSent == False: # If an email has not been sent yet.
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?") # Send temperature email.
            tempEmailSent = True # The email has been sent.
            emailRequestSent = True # Check for a response.
            print("Temperature email sent!") # CMD Line notification that emails have been sent.
        if lightEmailSent == False:
            sendEmail("The Light is under " + str(userLight) + "! Turn on the lights please.") # Send light email.
            lightEmailSent = True
            print("Light email sent!")
    elif temp > userTemp:
        light_notif = False # Don't send a LED notification.
        led_src = '/assets/light_off.png' # Changing the LED image.
        if tempEmailSent == False: # If an email has not been sent yet.
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?") # Sending temperature email.
            tempEmailSent = True # The email has been sent.
            emailRequestSent = True # Check for a response.
            print("Temperature Email Sent!") # CMD Line notification that an email has been sent.
    elif light < userLight:
        light_notif = True # Send a LED notification.
        led_src = '/assets/light_on.png' # Change the LED image.
        if lightEmailSent == False: # If an email has not been sent yet.
            sendEmail("The Light is under " + str(userLight) + "! Turn on the lights please.") # Send light email.
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
        fanTurnedOn = False # The fan is off.


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

    # Setting various labels.
    userTempText = "Temperature Threshold: " + str(userTemp)
    usernameText = "User: " + username
    userLightText = "Light Threshold: " + str(userLight)

    if fanTurnedOn:
        fanText = 'The fan is ON!'
    else:
        fanText = 'The fan is OFF!'

    return temp,humidity,light,led_src,light_notif,fan_src,userImage,userTempText,usernameText,userLightText,fanText



if __name__ == '__main__':
    app.run_server(debug=True)
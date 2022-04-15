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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','/assets/stylesheet2.css']


# Starting the application.
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets,dbc.themes.BOOTSTRAP])

#Layout of the application (Dash components, HTML).
app.layout = html.Div(children =[
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    ),
    html.H1(style={'text-align':'center'},children=["IoT Home Dashboard"]),
    html.Br(),html.Br(),
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
                        daq.Gauge(id='live-update-graph-temp', showCurrentValue=True, label='Temperature', max=50, min=0),
                        daq.Gauge(id='live-update-graph-humidity', showCurrentValue=True, label='Humidity',max=100, min=0),
                        html.Br()
                    ]),
                    html.Td(
                    style={'width':'33%','display': 'block','margin-left':'auto','margin-right':'auto'},
                    children=[
                        html.Br(),
                        html.Br(),
                        html.Img(id='fan_status', style={'width':'250px','height':'250px'})
                    ]),
                    html.Td(
                        style={'width':'33%','text-align': 'center'},
                        children=[
                            html.Br(),
                            daq.Gauge(id='live-update-graph-light', showCurrentValue=True, label='Light',max=4000, min=0),
                            html.P('LED Status'),
                            html.Img(id='led-status'),
                            dbc.Toast([html.P("An email has been sent.")], id='light-notification', header='Light is under 400!', dismissable=True, is_open=False,style={'width':'50%','height':'25%','margin-top':'auto'}),
                            html.Br()
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
         Output('fan_status','src')],
        [Input('interval-component', 'n_intervals')])

def update_graph_live(n):

    #----------- SET INITIAL VALUES ------------
    global emailSent
    global led_src
    global light_notif
    global fanTurnedOn

    emailSent = False
    fanTurnedOn = False



    # --------- DATA COLLECTION ----------------

    # Fetching light, humidity, and temp via MQTT.
    light = float(subscribe("light")) # Subscribing to the light topic

    data = loop()
    humidity = data[0]
    temp = data[1]

    # Printing the fetched values.
    print("Hum: ", humidity)
    print("Temp: ", temp)
    print("Light:", light)

    #  --------- NOTIFICATIONS OR ACTIONS ------------

    # Checking temperature and light and performing actions based on constraints.
    if temp > 24.0 and light < 400:
        if emailSent == False:
            setLED(True)
            led_src = '/assets/light_on.png'
            light_notif = True
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?")
            sendEmail("The Light is under 400! Turn on the lights please.")
            emailSent = True
            print("Temperature and Light Emails Sent!")
    elif temp > 24.0:
        if emailSent == False:
            setLED(False)
            light_notif = False
            led_src = '/assets/light_off.png'
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?")
            emailSent = True
            print("Temperature Email Sent!")
    elif light < 400:
        if emailSent == False:
            setLED(True)
            light_notif = True
            led_src = '/assets/light_on.png'
            sendEmail("The Light is under 400! Turn on the lights please.")
            emailSent = True
            print("Light Email Sent!")
    else:
        setLED(False)
        light_notif = False
        led_src = '/assets/light_off.png'

    # Changing the fan image depending on status.
    if (fanTurnedOn == True):
         fan_src = '/assets/fan_on.png'
    else:
        fan_src = '/assets/fan_off.png'

    return temp,humidity,light,led_src,light_notif,fan_src



if __name__ == '__main__':
    app.run_server(debug=True)
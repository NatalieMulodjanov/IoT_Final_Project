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
                        daq.Gauge(id='live-update-graph-humidity', showCurrentValue=True, label='Humidity',max=50, min=0),
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

emailSent = False
fanTurnedOn = False


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

    # --------- DATA COLLECTION ----------------

    # Fetching light, humidity, and temp via MQTT.
    light = float(subscribe("light")) # Subscribing to the light topic
    humidity = float(subscribe("humidity"))
    temp = float(subscribe("temperature"))

    # Printing the fetched values.
    print("Hum: ", humidity)
    print("Temp: ", temp)
    print("Light:", light)

    #  --------- NOTIFICATIONS OR ACTIONS ------------

    # Sending an email if temp is under 23.
    global emailSent
    if temp > 23:
        if emailSent == False:
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?")
            print("Email sent")
            emailSent = True

    # Changing the fan image depending on status.
    if (fanTurnedOn == True):
         fan_src = '/assets/fan_on.png'
    else:
        fan_src = '/assets/fan_off.png'

    # Changing LED status, sending email, showing notification depending on light value.
    if (light < 400):
        if emailSent == False:
            setLED(True)
            light_notif = True
            led_src = '/assets/light_on.png'
            sendEmail("The Light is under 400! Turn on the lights please.")
            emailSent = True
    else:
        setLED(False)
        light_notif = False
        led_src = '/assets/light_off.png'

    return temp,humidity,light,led_src,light_notif,fan_src



if __name__ == '__main__':
    app.run_server(debug=True)
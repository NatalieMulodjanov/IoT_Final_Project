import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from DHT11 import loop
from MQTTClient import subscribe
from led import setLED
from emailClient import sendEmail, receive_email


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Starting the application.
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
    html.Img(id='fan_status', style={'width': '100%'})
])

emailSent = False
fanTurnedOn = False

src = '/assets/fan_off.jpg'

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

    #light = float(subscribe("light")) # Subscribing to the light topic
    humidity = float(subscribe("humidity"))
    temp = float(subscribe("temperature"))
    global emailSent
    if temp > 23:
        if emailSent == False:
            sendEmail("Current temperature is; " + str(temp) + "C would you like to turn on the fan?")
            print("Email sent")
            emailSent = True
    
    print("Hum: ", humidity)
    print("Temp: ", temp)

    # notifications or actions
    #if (light < 400):
        #setLED(True)
        #sendEmail("The Light is under 400! Turn on the lights please.")
    #else:
        #setLED(False)


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
        value=10,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Light"}))

    global src
    global fanTurnedOn
    # receivedEmail = receive_email()
    # print(receivedEmail["Content"])
    # if "YES" in receivedEmail["Content"]:
    #     # print("Turning on the fan")
    #     # src='/assets/fan_on.jpg'
    #     fanTurnedOn = True
    #     # turnOnFan()

    return temperatureFig,humidityFig,lightFig



if __name__ == '__main__':
    app.run_server(debug=True)
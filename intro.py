import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
@app.callback(Output('live-update-graph-temp', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    temps = [1, 4, 6, 9, 15, 30, 60, 65.70, 100,
             120, 100, 80, 60, 40, 30, 20, 10, 5, 1]
    # Collect some data

    # Create the graph with subplots
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temps[n%len(temps)],
                            gauge={'axis': {'range': [-2, 11]},
                        'steps': [
                            {'range': [-2, 0], 'color': "white"},
                            {'range': [0, 7], 'color': "white"},
                            {'range': [7, 11], 'color': "white"}],
                        'threshold': {'line': {'color': "black", 'width': 1}, 'thickness': 1, 'value': 7}},
        # width=200,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Temperature"}))

    return fig


@app.callback(Output('live-update-graph-humidity', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    humidity = [1, 4, 6, 9, 15, 30, 60, 65.70, 100,
                120, 100, 80, 60, 40, 30, 20, 10, 5, 1]
    # Collect some data

    # Create the graph with subplots
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=humidity[n%len(humidity)],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Humidity"}))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

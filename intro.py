import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    speed = [1,4,6,9,15,30,60,65.70,100,120,100,80,60,40,30,20,10,5,1]
    # Collect some data


    # Create the graph with subplots
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = speed[n],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Speed"}))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
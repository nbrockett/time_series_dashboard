import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objects as go
import process_data as process_data
from dash.dependencies import Input, Output
import plotly
import random


from collections import deque

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = process_data.get_data()
df = df[df.unit_number == 3]
# df=(df-df.mean())/df.std()
df = (df-df.min())/(df.max()-df.min())

# time_deque = deque(df['time'].tolist())
# sensor_data_deque = deque(df['sensor_3'].tolist())

time_deque = deque(maxlen=150)
time_deque = time_deque + deque(list(range(1, len(df['sensor_3'].tolist())+1)))

print(time_deque)

full_sensor_data = deque(df['sensor_3'].tolist())
full_sensor_data2 = deque(df['sensor_4'].tolist())

sensor_data_deque = deque(maxlen=150)
sensor_data_deque = sensor_data_deque + deque(df['sensor_3'].tolist())
sensor_data_deque2 = deque(maxlen=150)
sensor_data_deque2 = sensor_data_deque2 + deque(df['sensor_4'].tolist())

print(sensor_data_deque)
print(sensor_data_deque2)



counter = 0

app.layout = html.Div(
    html.Div([
        html.H4('ASDASD Time Series Streaming example'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='interval-component',
            interval=600,
            n_intervals=0
        )
    ])
)

def update_data():

    global counter
    # print(counter)
    counter += 1

    global time_deque
    global sensor_data_deque
    print(time_deque[-1] + 1)
    time_deque.append(time_deque[-1] + 1)
    # sensor_data_deque.append(sensor_data_deque[-1] + sensor_data_deque[-1] * random.uniform(-0.1, 0.1))
    # sensor_data_deque2.append(sensor_data_deque2[-1] + sensor_data_deque2[-1] * random.uniform(-0.1, 0.1))

    sensor_data_deque.append(full_sensor_data[0])
    sensor_data_deque2.append(full_sensor_data2[0])

    full_sensor_data.rotate(-1)
    full_sensor_data2.rotate(-1)


    # time_deque = deque(df['time'].tolist())
    # sensor_data_deque = deque(df['sensor_3'].tolist())

last_n = [-1]
@app.callback(dash.dependencies.Output('live-graph', 'figure'), [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_graph_live(n):


    # print(n)
    # if n is None:
    #     return
    #
    # if n <= max(last_n):
    #     return

    last_n.append(n)


    # time_deque.rotate(1)
    # sensor_data_deque.rotate(1)

    update_data()

    # fig = go.Figure()
    # fig.add_trace(
    #     go.Scatter(
    #         x=list(time_deque),
    #         y=list(sensor_data_deque)
    #     )
    # )
    # return fig
    #
    data = go.Scatter(
        x=list(time_deque),
        y=list(sensor_data_deque),
        name='Scatter',
        mode='lines+markers'
    )

    data2 = go.Scatter(
        x=list(time_deque),
        y=list(sensor_data_deque2),
        name='Scatter',
        mode='lines+markers'
    )

    return {'data': [data, data2], 'layout': go.Layout(xaxis=dict(range=[min(time_deque), max(time_deque)]),
                                                yaxis=dict(range=[-0.2, 1.2]), )}


if __name__ == '__main__':
    app.run_server(debug=True)
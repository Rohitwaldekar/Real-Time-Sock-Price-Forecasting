import pandas as pd
import plotly.express as px
import pathlib

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# app = Dash(__name__)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dirname = pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()
df = pd.read_csv(str(dirname)+str("/data/raw/data.csv"),parse_dates=True, header=None)

df.columns = ['Datetime','Close']


df = pd.DataFrame({'year':[1,2,3,3,4,5],'lifeExp':[7,5,3,3,2,1],'country':[1,1,1,0,0,0]})

fig = px.line(df, x='year', y='lifeExp', color='country', symbol="country")

fig.update_layout(
    title='Stock Prices',
    xaxis_title='Date',
    yaxis_title='Price',
    template='plotly_white'
)

# Creating line plot
# fig = px.line(x=df['Datetime'], y=df['Close'])

# Updating layout
# fig.update_layout(
#     title='Stock Prices',
#     xaxis_title='Date',
#     yaxis_title='Price',
#     template='plotly_white',
#     xaxis_rangeslider_visible=True
# )

# import plotly.graph_objects as go

# fig = go.Figure()

# fig.add_trace(go.Scatter(
#     x=df['Datetime'], 
#     y=df['Close'],
#     name="Current"  
# ))

# fig.add_trace(go.Scatter(
#     x=[1, 2, 3, 4, 5],
#     y=[None,None,None , 4, 0],
#     name="Forecasted"
# ))

app.layout = html.Div([
    
    dcc.Interval(
        id= 'my_interval', 
        interval= 1000*30, 
        disabled= False, 
        n_intervals= 0, 
        max_intervals= -1
    ),

    dbc.Card(
        dbc.CardBody([
            html.H2(children='Real Time Sock Price Forcasting'),
            html.Div(children='''
                Select stock from below dropdown for forecasing.
            '''),
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'New York City', 'value': 'New York City'},
                    {'label': 'Montreal', 'value': 'Montreal'},
                    {'label': 'San Francisco', 'value': 'San Francisco'},
                ],
                clearable=False,
                value='Montreal',
                style={
                    'width': '60%'
                }
            )
        ]),
        color='#85CDFD'
    ),

    html.Div(
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='graph',
                    figure=fig
                )
            ]),
            style={
                'width': '100%' 
            },
        ),
        style={
            'margin-top': '20px'
        }
    )
    
        # html.H1(children='Hello Dash'),

        # html.Div(children='''
        #     Dash: A web application framework for your data.
        # '''),

        # dcc.Dropdown(
        #     id='dropdown',
        #     options=[
        #         {'label': 'New York City', 'value': 'New York City'},
        #         {'label': 'Montreal', 'value': 'Montreal'},
        #         {'label': 'San Francisco', 'value': 'San Francisco'},
        #     ],
        #     clearable=False,
        #     value='Montreal',
        #     style={'width': '40%', 'align': 'end'}
        # ),

        # html.Div(id='container', children=[]),

        # dcc.Graph(
        #     id='graph',
        #     figure={}
        # )
    ], style={
        'margin':'20px 20px 20px 20px'
})

@app.callback(
    Output(component_id='my_interval', component_property='n_intervals'),
    Input(component_id='dropdown', component_property='value')
)
def update_stock(num):
    print('N ',num)
    return 0        
    

# @app.callback(
#     Output(component_id='graph', component_property='figure'),
#     Input(component_id='my_interval', component_property='n_intervals')
# )
# def update_graph(num):
#     if num > -1:
#     #     raise PreventUpdate
#     # else:
#         df = pd.read_csv(str(dirname)+str("/data/raw/data.csv"),parse_dates=True, header=None)
#         df.columns = ['Datetime','Close']
#         fig = px.line(x=df['Datetime'], y=df['Close'])
#         fig.update_layout(
#             title='Stock Prices',
#             xaxis_title='Date',
#             yaxis_title='Price',
#             template='plotly_white',
#             # xaxis_rangeslider_visible=True
#         )
#         print('N ',num)
#         return (fig)

if __name__ == '__main__':
    app.run_server(debug=True)

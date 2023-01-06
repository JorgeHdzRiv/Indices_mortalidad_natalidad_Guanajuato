#-------------------------IMPORTS----------------------------------------#
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


#----------------------------APP MAIN-------------------------------------#
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#------------------------------DATA--------------------------------------#
estado = pd.read_csv('./data/mortalidad_estado.csv',index_col=0)
estado_defunciones = estado[estado['unidad_medida'] == 'Defunciones']
estado_porcentaje = estado[estado['unidad_medida'] == 'Porcentaje']

#-------------------------VARIABLES--------------------------------------#

options = estado_defunciones['indicador'].drop_duplicates().to_list()
available_indicators = estado_defunciones['indicador'].unique()

#-----------------------LAYOUT-------------------------------------------#
app.layout = html.Div(children=[
    html.H1('Analisis de defunciones en el estado de Guanajuato'),
    html.Div([
        html.H3('Defunciones a lo largo del tiempo en el estado de Guanajuato'),
        dcc.Graph(id="graph"),
        dcc.Checklist(
        id="checklist",
        options=options,
        value=["Defunciones generales", "Defunciones generales hombres","Defunciones generales mujeres"]
        )
    ]),
    
    html.Div([
        html.H3('Histograma a traves del tiempo por categoria'),
        dcc.Dropdown(
            id = 'indicator',
            options = [{'label': i,'value': i} for i in available_indicators],
            value='Defunciones generales'
        )
    ]),
    
    dcc.Graph(id='indicator-histogram'),
    
    html.Div([
        html.H1('Analisis por Municipios'),
    ]),
    
    
], style={'background-color': '#FFF0B2'})

#--------------------------CALLBACKS---------------------------------------#
@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))

def update_line_chart(indicadores):
    df = estado_defunciones # replace with your own data source
    mask = df['indicador'].isin(indicadores)
    fig = px.line(df[mask], 
        x="año", y="valor", color='indicador')
    return fig

@app.callback(
    Output("indicator-histogram",'figure'),
    Input('indicator','value')
)

def update_histogram(indicador):
    filtro = estado_defunciones[(estado_defunciones['indicador'] == indicador)]
    
    fig = px.bar(filtro,x='año',y='valor')
    
    fig.update_layout(transition_duration = 500)
    
    return fig


app.run_server(debug=True)
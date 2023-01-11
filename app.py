#--------------------------------IMPORTS---------------------------------#
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
#----------------------------APP MAIN-------------------------------------#
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#------------------------------DATA--------------------------------------#
estado = pd.read_csv('./data/mortalidad_estado.csv',index_col=0)
municipios = pd.read_csv('./data/mortalidad_municipios.csv',index_col=0)
estado_defunciones = estado[estado['unidad_medida'] == 'Defunciones']
estado_porcentaje = estado[estado['unidad_medida'] == 'Porcentaje']

#-------------------------VARIABLES--------------------------------------#
options = estado_defunciones['indicador'].drop_duplicates().to_list()
available_indicators = estado_defunciones['indicador'].unique()
indicators_porcent = estado_porcentaje['indicador'].unique()
available_municipios = municipios['desc_municipio'].unique()
years = municipios['año'].unique()

#-----------------------LAYOUT-------------------------------------------#
app.layout = html.Div(children=[
#------------------------------Estado-----------------------------------#
    html.H1('Analisis de defunciones en el estado de Guanajuato'),
    
    html.Div([
        html.H3('Defunciones a lo largo del tiempo en el estado de Guanajuato'),
        html.H4('Selecciona un indicador o varios para la grafica'),
        dcc.Checklist(
        id="checklist",
        options=options,
        value=["Defunciones generales", "Defunciones generales hombres","Defunciones generales mujeres"]
        ),
        
    ]),
    
    dcc.Graph(id="graph"),
    
    
    html.Div([
        html.H3('Histograma a traves del tiempo por categoria'),
        dcc.Dropdown(
            id = 'indicator',
            options = [{'label': i,'value': i} for i in available_indicators],
            value='Defunciones generales'
        )
    ]),
    
    dcc.Graph(id='indicator-histogram'),
    
    #Grafica de porcentajes por categoria de defunciones
    html.Div([
        html.H3('Porcentaje de los indicadores en el tiempo'),
        html.Div(children='''
         Se puede observar a lo largo de un deslizador de tiempo la variacion y el porcentaje 
         de cada indicador en todo el estado.
        '''),
        
        dcc.Slider(
            id='year-slider',
            min=estado_defunciones['año'].min(),
            max=estado_defunciones['año'].max(),
            value=estado_defunciones['año'].min(),
            marks={str(año): str(año) for año in estado_defunciones['año'].unique()},
            step=None
        ),
    ]),
    
    dcc.Graph(id='pie-with-slider'),
    
    # Analisis de los porcentajes
    html.Div([
        html.H3('Histograma a traves del tiempo por indicador de porcentaje'),
        dcc.Dropdown(
            id = 'indicator_porcent',
            options = [{'label': i,'value': i} for i in indicators_porcent],
            value='Índice de sobremortalidad masculina'
        )
    ]),
    
    dcc.Graph(id='indicator-histogram-porcent'),
    
#---------------------------------Municipios------------------------------#
    html.H1('Analisis de defunciones en los muncipios de Guanajuato'),
    
    #-------------------Grafico lineal-----------------------------------#
    html.H3('Defunciones a traves del tiempo por municipio e indicadores'),
    
    html.Div([
        html.H5('Selecciona un indicador o varios'),
        dcc.Checklist(
        id="checklist_mun",
        options=options,
        value=["Defunciones generales", "Defunciones generales hombres","Defunciones generales mujeres"]
        ),
    ],style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
       html.H5('Selecciona un municipio'),
       dcc.Dropdown(
            id = 'municipio_line',
            options = [{'label': i,'value': i} for i in available_municipios],
            value='Irapuato'
        ) 
    ],style={'width': '48%', 'float':'right', 'display': 'inline-block'}),
    
    dcc.Graph(id='line_municipio'),
    
    #----------------------Histograma-----------------------------------------#
    
    html.H3('Histograma a traves del tiempo por indicador y por municipio'),
    
    html.Div([ 
        html.H5('Selecciona un indicador'),
        dcc.Dropdown(
            id = 'indicador',
            options = [{'label': i,'value': i} for i in available_indicators],
            value='Defunciones generales'
        )
        
    ],style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        html.H5('Selecciona un municipio'),
        dcc.Dropdown(
            id = 'municipio',
            options = [{'label': i,'value': i} for i in available_municipios],
            value='Irapuato'
        )
        
    ],style={'width': '48%', 'display': 'inline-block'}),
    
    dcc.Graph(id='municipio-histogram'),
    
    #------------------------------Grafico circular ------------------------------------------#
    html.H3('Municipios superiores al promedio de cada indicador en el año correspondiente'),
    
    html.P('Para visualizar datos seleccione alguna opcion'),
    html.Div([
        html.H5('Selecciona un año'),
        dcc.Dropdown(
            id = 'year',
            options = [{'label': i,'value': i} for i in years],
            value='2020'
        )
    ],style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        html.H5('Selecciona un indicador'),
        dcc.Dropdown(
            id = 'indicador_circ',
            options = [{'label': i,'value': i} for i in available_indicators],
            value='Defunciones generales'
        )
    ],style={'width': '48%', 'display': 'inline-block'}),
    
    dcc.Graph(id='municipio-porcentaje'),
    
#------------------NO ESPECIFICADO-----------------------------------------#
    
    
], style={'background-color': '#FFF0B2'})

"""
#--------------------------CALLBACKS---------------------------------------#
"""
#-------------------------------ESTADO-------------------------------------#
@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))

def update_line_chart(indicadores):
    df = estado_defunciones # replace with your own data source
    mask = df['indicador'].isin(indicadores)
    fig = px.line(df[mask], 
        x="año", y="valor", color='indicador',title=f'Indicadores a traves del tiempo en Guanajuato')
    return fig

@app.callback(
    Output("indicator-histogram",'figure'),
    Input('indicator','value')
)

def update_histogram(indicador):
    filtro = estado_defunciones[(estado_defunciones['indicador'] == indicador)]
    
    fig = px.bar(filtro,x='año',y='valor',color='valor',labels={'valor':'Numero de defunciones'},title=f'Histograma del indicador:{indicador},en todo el estado de Guanajuato')
    
    fig.update_layout(transition_duration = 500)
    
    return fig

@app.callback(
    Output('pie-with-slider', 'figure'),
    Input('year-slider', 'value')
)

def update_figure(selected_year):
    filtered_df = estado_defunciones[estado_defunciones.año == selected_year]

    #filtered_df.loc[filtered_df['valor'] < 200, 'desc_municipio'] = 'Otros' # Represent only large countries
    fig = px.pie(filtered_df, values='valor', names='indicador', title=f'Porcentaje de los indicadores en todo el estado de Guanajuato en {selected_year}')             


    fig.update_layout(transition_duration=500)

    return fig

#------------------Porcentajes-----------------------------#
@app.callback(
    Output("indicator-histogram-porcent",'figure'),
    Input('indicator_porcent','value')
)

def update_histogram(indicador_porcentaje):
    filtro = estado_porcentaje[(estado_porcentaje['indicador'] == indicador_porcentaje)]
    
    fig = px.bar(filtro,x='año',y='valor',color='valor',labels={'valor':'Porcentaje'},title=f'Valor porcentual de {indicador_porcentaje}')
    
    fig.update_layout(transition_duration = 500)
    
    return fig

#------------------------------Municipios--------------------------------------------#
@app.callback(
    Output('line_municipio','figure'),
    Input('checklist_mun','value'),
    Input('municipio_line','value')
)

def update_line_chart(indicadores,municipio):
    filtro = municipios[(municipios['desc_municipio'] == municipio)]
    mask = filtro['indicador'].isin(indicadores)
    fig = px.line(filtro[mask], 
        x="año", y="valor", color='indicador',title=f'Indicadores a traves del tiempo en: {municipio}')
    return fig
#-----------------Histrograma Callback----------------#
@app.callback(
    Output('municipio-histogram','figure'),
    Input('indicador','value'),
    Input('municipio','value')
)

def update_histogram(indicador,municipio):
    filtro = municipios[(municipios['indicador'] == indicador)]
    filtro_final = filtro[(filtro['desc_municipio'] == municipio)]
    
    fig = px.bar(filtro_final,x='año',y='valor',color='valor',labels={'valor':'Numero de defunciones'},title=f'Histograma del indicador:{indicador}, en:{municipio}')
    
    fig.update_layout(transition_duration = 500)
    
    return fig
#--------------------------Circular Callback-------------------------------#
@app.callback(
    Output('municipio-porcentaje','figure'),
    Input('year','value'),
    Input('indicador_circ','value')
)

def update_pie(year,indicador):
    filtro = municipios[(municipios['año'] == year)]
    filtro_final = filtro[(filtro['indicador'] == indicador)]
    promedio = filtro_final['valor'].mean()
    filtro_final.loc[filtro_final['valor'] < promedio, 'desc_municipio'] = 'Municipios debajo del promedio' # Represent only large countries
    
    fig = px.pie(filtro_final, values='valor', names='desc_municipio', title=f'Municipios del indicador:{indicador} en {year},mayores al promedio:{promedio:.2f}')
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(transition_duration=500)
    
    return fig

#---------------------------NO ESPECIFICADO CALLBACKS--------------------#

"""#---------------------------MAIN--------------------------------------#"""
if __name__ == '__main__':
    app.run_server(debug=True)

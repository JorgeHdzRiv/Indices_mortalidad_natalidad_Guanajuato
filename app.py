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
estado_defunciones = estado[estado['unidad_medida'] == 'Defunciones']
estado_porcentaje = estado[estado['unidad_medida'] == 'Porcentaje']

#-------------------------VARIABLES--------------------------------------#
options = estado_defunciones['indicador'].drop_duplicates().to_list()
available_indicators = estado_defunciones['indicador'].unique()
indicators_porcent = estado_porcentaje['indicador'].unique()

#-----------------------LAYOUT-------------------------------------------#
app.layout = html.Div(children=[
    
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

@app.callback(
    Output('pie-with-slider', 'figure'),
    Input('year-slider', 'value')
)

def update_figure(selected_year):
    filtered_df = estado_defunciones[estado_defunciones.año == selected_year]

    #filtered_df.loc[filtered_df['valor'] < 200, 'desc_municipio'] = 'Otros' # Represent only large countries
    fig = px.pie(filtered_df, values='valor', names='indicador', title='Porcentaje de los indicadores')             

    fig.update_layout(transition_duration=500)

    return fig

#------------------Porcentajes-----------------------------#
@app.callback(
    Output("indicator-histogram-porcent",'figure'),
    Input('indicator_porcent','value')
)

def update_histogram(indicador_porcentaje):
    filtro = estado_porcentaje[(estado_porcentaje['indicador'] == indicador_porcentaje)]
    
    fig = px.bar(filtro,x='año',y='valor')
    
    fig.update_layout(transition_duration = 500)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
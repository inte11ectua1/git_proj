from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, all_cont

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
                html.Div([
                html.H1("Статистика по континентам"),
                html.H3("Визуализация динамики основных показателей по странам мира с 2000 по 2015 годы."),
                html.H5(" Используйте фильтр, чтобы увидеть результат."),
                html.Hr(style = {'color' : 'black'}),
            ], style = {'textAlign' : 'center'})
        )
    ]),

    dbc.Row ([    
        html.Div([
            html.Div([
                html.H3('Континенты'),
                dcc.Dropdown(
                    id = 'crossfilter-cont',
                    options = [{'label': i, 'value': i} for i in all_cont],
                    # значение континента, выбранное по умолчанию
                    value = ['Europe'],
                    # возможность множественного выбора
                    placeholder = "Выбери континент",
                    multi = True,
                    clearable = False,
                    style = {'color': 'Magenta'}
                )
            ],
            style = {'width': '48%', 'display': 'inline-block'}),
       
            html.Div([
                html.H3('Основные показатели'),
                dcc.RadioItems(
                    options = [
                        {'label':'Продолжительность жизни', 'value': 'Life expectancy'},
                        {'label':'Население', 'value': 'Population'},
                        {'label':'ВВП', 'value': 'GDP'},
                        {'label':'Школьное образование', 'value': 'Schooling'},
                    ],
                    id = 'crossfilter-ind',
                    value = 'GDP',
                    #labelStyle={'display': 'inline-block'}
                )
            ], style = {'width': '48%',  'float': 'right', 'display': 'inline-block'}),
        ], style = {
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'transparent',
            'padding': '10px 5px'
        }),
    ]),
    
    html.Br(),

    html.Div(
        dcc.Slider(
            id = 'crossfilter-year',
            min = df['Year'].min(),
            max = df['Year'].max(),
            value = 2000,
            step = None,
            marks = {str(year):
                str(year) for year in df['Year'].unique()}
        ), style = {'width': '95%', 'padding': '0px 20px 20px 20px', 'text_color':'black'}
        ),
    html.Div(
        dcc.Graph(id = 'bar'),
        style = {'width': '49%', 'display': 'inline-block'}
    ),
       
    html.Div(
        dcc.Graph(id = 'line'),
        style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}
    ),


    html.Div(
        dcc.Graph(id = 'choropleth2'),
        style = {'width': '100%', 'display': 'inline-block'}
    ),

], fluid=True)

@callback(
    Output('bar', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_stacked_area(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['continent'].isin(continent))]
    figure = px.bar(
        filtered_data,
        x = 'Year',
        y = indication,
        color = 'Country'
        )
    return figure

@callback(
    Output('line', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_scatter(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['continent'].isin(continent))]
    figure = px.line(
        filtered_data,
        x = "Year",
        y = indication,
        color = "Country",
        title = "Значения показателя по странам",
        markers = True,
    )
    figure.update_layout(title_text='Значения показателя по странам', title_x=0.5)
    return figure
@callback(
    Output('choropleth2', 'figure'),
    Input('crossfilter-ind', 'value')
)
def update_choropleth(indication):
    figure = px.choropleth(
        df,
        locations='Country',
        locationmode = 'country names',
        color = indication,
        hover_name='Country',
        labels = {'Country':'Страна', 'Year':'Год',
                    'Population':'Население', 'Life expectancy':'Продолжительность жизни',
                    'GDP':'ВВП', 'Schooling':'Продолжительность обучения'},
        title = 'Показатели по странам',
        color_continuous_scale=px.colors.sequential.Magenta,
        animation_frame = 'Year',
        height=650
        )
    figure.update_layout(title_text='Показатели по странам', title_x=0.5)

    return figure
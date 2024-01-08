# Import essential Python packages
import pathlib
import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# import plotly.express as px


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Read the data

# US Honey datac
honey_data = pd.read_csv('data/US_honey_dataset_updated.csv')

# North America Temperature Anomalies data
temperature_data = pd.read_csv('data/North_America_Temperature_Anomalies.csv')

# List of all the states
states = list(honey_data['state'].unique())
states.insert(0, 'All')


# Line Function for the line plots
# Building the production overtime graph
def line_plots(input_states, year_col, target_col, the_title, y_axis, x_axis):
    if input_states == 'All':
        # Calculate for all the states
        target = honey_data.groupby(year_col)[[target_col]].sum().reset_index()
        # Calculations for the percentage change
        first_value = int(target.loc[
                              target[year_col] == target[year_col].min(), target_col
                          ])
        last_value = int(target.loc[
                             target[year_col] == target[year_col].max(), target_col
                         ])

        # Production overtime figure
        target_fig = go.Figure()
        # Production overtime line plot
        target_fig.add_trace(go.Scatter(x=target[year_col],
                                        y=target[target_col],
                                        line=dict(color='#D9560B', width=3), connectgaps=True))
        # Graph marker
        target_fig.add_trace(go.Scatter(x=[target[year_col].max()],
                                        y=[int(target.loc[
                                                   target[year_col] == target[
                                                       year_col].max(),
                                                   target_col
                                               ])],
                                        mode='markers',
                                        marker=dict(color='#D9560B', size=10)))
        target_fig.update_layout(title=dict(
            text=the_title,
            font=dict(size=20, color='#0C0B09')
        ),
            xaxis_title=dict(
                text=x_axis,
                font=dict(size=14, color='#595959')
            ), yaxis_title=dict(
                text=y_axis,
                font=dict(size=14, color='#595959')
            ),
            plot_bgcolor='white',
            showlegend=False,
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='#D9D9D9',
                linewidth=2,
                ticks='outside',
                tickcolor='#595959',
                tickfont=dict(
                    color='#595959'
                )
            ),
            yaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='#D9D9D9',
                linewidth=2,
                tickfont=dict(
                    color='#595959'
                )
            ))
        # Annotation
        target_fig.add_annotation(x=target['year'].max() + 2,
                                  y=int(target.loc[
                                            target['year'] == target[
                                                'year'].max(),
                                            target_col
                                        ]),
                                  text='{}%'.format(
                                      round(((last_value - first_value) / first_value) * 100, 1)
                                  ),
                                  showarrow=False,
                                  font=dict(size=14, color='#D9560B')
                                  )

        return target_fig

    else:
        # Calculate for a specific state
        target = honey_data.loc[honey_data['state'] == input_states].groupby(year_col)[
            [target_col]].sum().reset_index()
        # Calculate for the percentage change
        first_value = int(target.loc[
                              target[year_col] == target[year_col].min(), target_col
                          ])
        last_value = int(target.loc[
                             target[year_col] == target[year_col].max(), target_col
                         ])

        # Production overtime figure
        target_fig = go.Figure()
        # Production overtime line plot
        target_fig.add_trace(go.Scatter(x=target[year_col],
                                        y=target[target_col],
                                        line=dict(color='#D9560B', width=3), connectgaps=True))
        # Graph marker
        target_fig.add_trace(go.Scatter(x=[target[year_col].max()],
                                        y=[int(target.loc[
                                                   target[year_col] == target[
                                                       year_col].max(),
                                                   target_col
                                               ])],
                                        mode='markers',
                                        marker=dict(color='#D9560B', size=10)))
        target_fig.update_layout(title=dict(
            text=the_title,
            font=dict(size=20, color='#0C0B09')
        ),
            xaxis_title=dict(
                text=x_axis,
                font=dict(size=14, color='#595959')
            ), yaxis_title=dict(
                text=y_axis,
                font=dict(size=14, color='#595959')
            ),
            plot_bgcolor='white',
            showlegend=False,
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='#D9D9D9',
                linewidth=2,
                ticks='outside',
                tickcolor='#595959',
                tickfont=dict(
                    color='#595959'
                )
            ),
            yaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='#D9D9D9',
                linewidth=2,
                tickfont=dict(
                    color='#595959'
                )
            ))
        # Annotation
        target_fig.add_annotation(x=target[year_col].max() + 2,
                                  y=int(target.loc[
                                            target[year_col] == target[
                                                year_col].max(), target_col
                                        ]),
                                  text='{}%'.format(
                                      round(((last_value - first_value) / first_value) * 100, 1)
                                  ),
                                  showarrow=False,
                                  font=dict(size=14, color='#D9560B')
                                  )

        return target_fig


app.layout = html.Div(children=[
    # The title section
    dbc.Row(
        dbc.Col(
            html.Div('United States Honey Production',
                     style={'font-size': '60px', 'font-family': 'Merriweather', 'font-weight': 'bold',
                            'margin-top': '50px', 'color': 'white'}),
            width={'size': 10, 'offset': 1},
            style={'background-color': '#A63F03', 'padding': '0 0 0 50px'},
            xs=8, sm=8, md=8, lg=10, xl=10
        ), justify='center'
    ),
    # Horizontal line separating the title and the description
    dbc.Row(dbc.Col(html.Hr(),
                    width={'size': 10, 'offset': 1},
                    style={'background-color': '#A63F03', 'color': 'white'},
                    xs=8, sm=8, md=8, lg=10, xl=10
                    ), justify='center'
            ),
    # Description section of the report
    dbc.Row(
        dbc.Col(
            html.Div([
                html.P("""Since 1994, the U.S. has experienced a significant decrease in honey production, from 210 
                million to 23 million pounds in 2021, which also marks the lowest production level ever recorded. The 
                quantity produced has been fluctuating and gradually decreased from 1994 to 2008. However, 
                due to honey bee diseases in 2008, there was a sharp drop in the following years (2009 and 2010), 
                from 160 million to 44 million pounds in 2010, or a 72.0187% drop. Since then, production has 
                remained low, and the average pounds was about 35 million pounds per year.""")
            ], style={'color': 'white'}),
            width={'size': 10, 'offset': 1},
            style={'background-color': '#A63F03', 'padding': '0 50px 20px 50px'},  # padding [top right bottom left]
            xs=8, sm=8, md=8, lg=10, xl=10
        ), justify='center'
    ),
    html.Br(),
    # The overview section
    dbc.Row([
        # Total Production Overview
        dbc.Col([
            html.Div('Total Production'),
            html.Div(id='total-production', style={'font-size': '28px', 'font-weight': 'bold'})
        ], style={'background-color': '#D9D9D9', 'padding': '20px 0', 'color': '#A63F03',
                  'text-align': 'center', 'border-radius': '12px 0 0 12px'},
            width={'size': 2, 'offset': 1},
            xs=8, sm=8, md=8, lg=2, xl=2),
        # Colonies Number Overview
        dbc.Col([
            html.Div('Total Number of Colonies'),
            html.Div(id='total-colonies', style={'font-size': '28px', 'font-weight': 'bold'})
        ], style={'background-color': '#D9D9D9', 'padding': '20px 0', 'color': '#A63F03',
                  'text-align': 'center'},
            width={'size': 2},
            xs=8, sm=8, md=8, lg=2, xl=2),
        # Total Stock Overview
        dbc.Col([
            html.Div('Total Stocks'),
            html.Div(id='total-stock', style={'font-size': '28px', 'font-weight': 'bold'})
        ], style={'background-color': '#D9D9D9', 'padding': '20px 0', 'color': '#A63F03',
                  'text-align': 'center'},
            width={'size': 2},
            xs=8, sm=8, md=8, lg=2, xl=2),
        # Value of Production Overview
        dbc.Col([
            html.Div('Total Value of Production'),
            html.Div(id='total-value-production', style={'font-size': '28px', 'font-weight': 'bold'})
        ], style={'background-color': '#D9D9D9', 'padding': '20px 0', 'color': '#A63F03',
                  'text-align': 'center', 'border-radius': '0 12px 12px 0'},
            width={'size': 2},
            xs=8, sm=8, md=8, lg=6, xl=2),
        # State and dropdown
        dbc.Col([
            html.Div('Choose a State: ', style={'margin-right': '10px', 'margin-bottom': '10px'}),
            html.Div(dcc.Dropdown(
                id='input-state',
                options=[{'label': i, 'value': i} for i in states],
                value='All'
                # multi=True
            ), style={'width': '100%', 'margin-right': '10px'})
        ], style={'background-color': '#F2F2F2',
                  'padding': '20px 0 0 20px'},
            width={'size': 2},
            xs=8, sm=8, md=8, lg=2, xl=2),
    ], justify='center'),
    html.Br(),

    # Row 1 for the viz
    dbc.Row([
        # First Column
        dbc.Col([
            # Total Production overtime plot
            html.Div(dcc.Graph(id='production-overtime')),
            # Number of colonies overtime plot
            html.Div(dcc.Graph(id='colonies-number'))
        ],
            width={'size': 5, 'offset': 1},
            xs=8, sm=8, md=8, lg=5, xl=5
        ),
        # Second Column
        dbc.Col([
            # Total Production by states map
            dbc.Row([
                dbc.Col(html.Div(dcc.Graph(id='top-production')))
            ]),
            # Total Production by states bar-chart
            dbc.Row([
                dbc.Col(html.Div(dcc.Graph(id='production-on-map')))
            ])
        ],
            width={'size': 5},
            xs=8, sm=8, md=8, lg=5, xl=5
        )
    ], justify='center'),
    html.Br(),
    html.Br(),
    # Row 2 for viz
    dbc.Row([
        # Bubble plot
        dbc.Col([
            html.H2('Number of Colonies and Production',
                    style={'font-family': 'Merriweather'}),
            html.Div("""There is a strong relationship between the number of colonies that a state has with the total
                production values. As the number of colonies increases so is the total production of honey. The
                correlation value is of 0.99, which is almost 1.
                """),
            html.Br(),
            html.Div(dcc.Graph(id='production-colonies'))
        ],
            width={'size': 5, 'offset': 1},
            xs=8, sm=8, md=8, lg=5, xl=5
        ),
        # Heat Anomalies plot
        dbc.Col([
            html.H2('The Effect of Rising Temperatures',
                    style={'font-family': 'Merriweather'}),
            html.Div("""The preferred temperature range for Honey bees to maintain their hives is 32-36C (
            89.6-96.8F). Honey bee larvae will not develop and can die when exposed to temperatures outside this 
            range. Climate change has affected the whole planet earth."""),
            html.Br(),
            html.Div(dcc.Graph(id='temperature-anomalies'))
        ],
            width={'size': 5},
            xs=8, sm=8, md=8, lg=5, xl=5
        )
    ], justify='center'),
    # Line breaks
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(html.Hr(),
                    width={'size': 10, 'offset': 1},
                    style={'background-color': '#A63F03', 'color': 'white'})),
    dbc.Row(
        dbc.Col(
            html.Div([
                html.P("""The footer""")
            ], style={'color': 'white'}),
            width={'size': 10, 'offset': 1},
            style={'background-color': '#A63F03', 'text-align': 'center',
                   'padding': '50px 50px 50px 50px'}  # padding [top right bottom left]
        )
    )
], style={'background-color': '#F2F2F2'})


# Callback function definition
@app.callback([
    Output(component_id='total-production', component_property='children'),
    Output(component_id='total-colonies', component_property='children'),
    Output(component_id='total-stock', component_property='children'),
    Output(component_id='total-value-production', component_property='children')
],
    Input(component_id='input-state', component_property='value'))
# Add computation to callback function and return values
def overview(state_input):
    if state_input == 'All':
        # Calculate the stat for all the states
        total_production = honey_data['production'].sum()
        total_colonies = honey_data['colonies_number'].sum()
        total_stocks = honey_data['stocks'].sum()
        total_value_production = honey_data['value_of_production'].sum()

        return ['{:,}M'.format(round(total_production / 1000000, 1)),
                '{:,}M'.format(round(total_colonies / 1000000, 1)),
                '{:,}M'.format(round(total_stocks / 1000000, 1)),
                '{:,}M'.format(round(total_value_production / 1000000, 1))]
    else:
        # Calculate the stats for an individual state
        total_production = honey_data.loc[honey_data['state'].isin([state_input]), 'production'].sum()
        total_colonies = honey_data.loc[honey_data['state'].isin([state_input]), 'colonies_number'].sum()
        total_stocks = honey_data.loc[honey_data['state'].isin([state_input]), 'stocks'].sum()
        total_value_production = honey_data.loc[honey_data['state'].isin([state_input]), 'value_of_production'].sum()

        return ['{:,}M'.format(round(total_production / 1000000, 1)),
                '{:,}M'.format(round(total_colonies / 1000000, 1)),
                '{:,}M'.format(round(total_stocks / 1000000, 1)),
                '{:,}M'.format(round(total_value_production / 1000000, 1))]


# Callback for production overtime graph
@app.callback(Output(component_id='production-overtime', component_property='figure'),
              Input(component_id='input-state', component_property='value'))
# Building the production overtime graph
def production_overtime_graph(state_input):
    return line_plots(state_input, 'year', 'production', 'US Honey Production by Year', 'Total Production', 'Year')


# Callback for Number of colonies graph
@app.callback(Output(component_id='colonies-number', component_property='figure'),
              Input(component_id='input-state', component_property='value'))
# Function for Number of colonies graph
def colonies_number_graph(state_input):
    return line_plots(state_input, 'year', 'colonies_number', 'Total Colonies Over time', 'Total Colonies', 'Year')


# Callback for total production by state on map
@app.callback(Output(component_id='production-on-map', component_property='figure'),
              Input(component_id='input-state', component_property='value'))
# Function for total production by state on map
def production_map(state_input):
    # Latitude and Longitude of US States
    states_lat_long = pd.read_csv('data/states.csv')

    # The data
    us_map = honey_data.groupby('state')[['production']].sum().reset_index()
    # Merge the data
    us_map = us_map.merge(states_lat_long, left_on='state', right_on='state_name')
    # Drop some state_name column
    us_map.drop('state_name', axis=1, inplace=True)
    # Rename columns
    us_map.rename(columns={'state_x': 'state', 'state_y': 'code'}, inplace=True)

    if state_input == 'All':
        # The map
        us_map_fig = go.Figure(data=go.Choropleth(
            locations=us_map['code'],
            z=us_map['production'],
            locationmode='USA-states',
            colorscale='Oranges',
            text=us_map['state']
        ))

        us_map_fig.update_layout(
            title=dict(
                text='Total Honey Production States by States',
                font=dict(size=20, color='#0C0B09')
            ),
            geo_scope='usa',
            margin={"r": 0, "t": 30, "l": 0, "b": 0}
        )

        return us_map_fig
    else:
        us_map = us_map.loc[us_map['state'] == state_input]

        # The map
        us_map_fig = go.Figure(data=go.Choropleth(
            locations=us_map['code'],
            z=us_map['production'],
            locationmode='USA-states',
            colorscale='Oranges',
            text=us_map['state'],
            showscale=False
        ))

        us_map_fig.update_layout(
            title=dict(
                text='Total Honey Production States by States',
                font=dict(size=20, color='#0C0B09')
            ),
            geo_scope='usa',
            margin={"r": 0, "t": 30, "l": 0, "b": 0}
        )

        return us_map_fig


# Callback for top production by states
@app.callback(Output(component_id='top-production', component_property='figure'),
              Input(component_id='input-state', component_property='value'))
# Function for top production by states
def top_production_graph(state_input):
    if state_input == 'All':
        top_production = honey_data.groupby('state')[
            ['production']].sum().reset_index().sort_values('production', ascending=False).head()
        top_production = top_production.sort_values('production', ascending=True)

        top_production_fig = go.Figure()
        top_production_fig.add_trace(go.Bar(x=top_production['production'], y=top_production['state'],
                                            marker=dict(color=['#B4BEC9', '#B4BEC9', '#B4BEC9', '#D9560B', '#D9560B']),
                                            name='Top Five Honey Production States',
                                            orientation='h',
                                            text=['{:,}M'.format(round(i / 1000000, 1)) for i in
                                                  top_production['production']],
                                            textfont=dict(color='white', size=14),
                                            textposition='inside')  # more ['inside', 'outside', 'none']
                                     )

        top_production_fig.update_layout(
            title=dict(
                text='Top Five Honey Production States',
                font=dict(size=20, color='#0C0B09')
            ),
            xaxis_title=dict(
                text='Total Production',
                font=dict(size=14, color='#595959')
            ),
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='#D9D9D9',
                linewidth=2,
                ticks='outside',
                tickcolor='#595959',
                tickfont=dict(
                    color='#595959'
                )
            ),
            yaxis=dict(
                showline=False,
                showgrid=False,
                showticklabels=True,
                linecolor='#D9D9D9',
                linewidth=2,
                tickfont=dict(
                    color='#595959'
                )
            ),
            plot_bgcolor='white'
        )

        return top_production_fig


# Production vs Colonies Number Callback
@app.callback(Output(component_id='production-colonies', component_property='figure'),
              Input(component_id='input-state', component_property='value'))
# Function Production vs Colonies Number Graph
def production_colonies_graph(state_input):
    production_colonies = honey_data.groupby('state')[['production', 'colonies_number']].sum().reset_index()

    # The size of the dots
    size = production_colonies['production'] + production_colonies['colonies_number']

    # Plot
    production_colonies_fig = go.Figure(data=[go.Scatter(
        x=production_colonies['production'],
        y=production_colonies['colonies_number'],
        mode='markers',
        text=production_colonies['state'],
        marker=dict(
            size=size,
            sizemode='area',
            sizeref=2. * max(size) / (70. ** 2),
            color='#D9560B'
        )
    )])

    production_colonies_fig.update_layout(title=dict(
        text='Production vs Number of Colonies by States',
        font=dict(size=20, color='#0C0B09')
    ),
        xaxis_title=dict(
            text='Number of Colonies',
            font=dict(size=14, color='#595959')
        ), yaxis_title=dict(
            text='Total Production',
            font=dict(size=14, color='#595959')
        ),
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#D9D9D9',
            linewidth=2,
            ticks='outside',
            tickcolor='#595959',
            tickfont=dict(
                color='#595959'
            )
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#D9D9D9',
            linewidth=2,
            tickfont=dict(
                color='#595959'
            )
        ))

    return production_colonies_fig


# Temperature Anomalies Callback
@app.callback(Output(component_id='temperature-anomalies', component_property='figure'),
              Input(component_id='input-state', component_property='value'))
# Temperature Anomalies Graph Function
def temperature_anomalies_graph(state_input):
    temperature_anomalies_fig = go.Figure(data=go.Scatter(
        x=temperature_data['Year'], y=temperature_data['Value'],
        mode='markers',
        marker=dict(
            size=12,
            color=temperature_data['Value'],
            colorscale='RdBu',
            reversescale=True,
            showscale=True,
            colorbar=dict(
                tickvals=[-1.3, 1.99],
                ticktext=['colder', 'warmer'],
                ticks='outside'
            )
        )
    ))

    temperature_anomalies_fig.add_hline(y=0, line_color='#8C8C8C', line_width=1,
                                        annotation_text="baseline",
                                        annotation_position="bottom right",
                                        annotation_font_size=14,
                                        annotation_font_color="#8C8C8C")

    temperature_anomalies_fig.update_layout(title=dict(
        text='Temperature Anomalies From 1910 to 2022',
        font=dict(size=20, color='#0C0B09')
    ),
        xaxis_title=dict(
            text='Year',
            font=dict(size=14, color='#595959')
        ), yaxis_title=dict(
            text='Anomalies Values',
            font=dict(size=14, color='#595959')
        ),
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#D9D9D9',
            linewidth=2,
            ticks='outside',
            tickcolor='#595959',
            tickfont=dict(
                color='#595959'
            )
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#D9D9D9',
            linewidth=2,
            tickfont=dict(
                color='#595959'
            )
        ),
        coloraxis_colorbar=dict(
            title='anomalies'
        ))

    return temperature_anomalies_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

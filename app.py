# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from figures.general_timeline import get_general_figures
from figures.timelines import get_house_timeline, get_people_timeline
from simulator.main import run
from simulator.setup import MONTHS_A_PERSON_LIVES, DEFAULT_SETUP
from simulator.simulation import Ruleset
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

allow_inheritance = False
ruleset = Ruleset.by_shares

stats = run(verbose=False)
human, money = get_general_figures(stats)
house_timeline = get_house_timeline(stats)
people_timeline = get_people_timeline(stats, allow_inheritance, ruleset)


def markdown(text):
    return html.Div([
        dcc.Markdown(children=text)
    ])


@app.callback(
    [
        Output('human', 'figure'),
        Output('money', 'figure'),
        Output('house_timeline', 'figure'),
        Output('people_timeline', 'figure'),
        Output("loading-output-1", "children")
    ],
    [Input('submit-button-state', 'n_clicks')],
    [
        State(component_id='inheritance', component_property='value'),
        State(component_id='ruleset', component_property='value'),
        State(component_id='max_people', component_property='value'),
        State(component_id='min_people', component_property='value'),

        State(component_id='initial_number_of_people', component_property='value'),
        State(component_id='initial_number_of_houses', component_property='value'),
        State(component_id='minimum_free_houses_policy', component_property='value'),
        State(component_id='number_of_months_to_run', component_property='value'),
        State(component_id='average_house_cost', component_property='value'),
        State(component_id='sigma_house_cost', component_property='value'),
        State(component_id='number_of_shares_per_house', component_property='value')
    ]
)
def update(n_clicks, inheritance, ruleset, max_people,min_people, initial_number_of_people, initial_number_of_houses,
           minimum_free_houses_policy, number_of_months_to_run, average_house_cost, sigma_house_cost,
           number_of_shares_per_house):
    ruleset = Ruleset.by_shares if ruleset == '1' else Ruleset.normal_rent
    allow_inheritance = False if inheritance == '1' else True

    setup = DEFAULT_SETUP.copy()
    setup['allow_inheritance'] = allow_inheritance
    setup['ruleset'] = ruleset

    setup['max_people'] = int(max_people)
    setup['min_people'] = int(min_people)

    setup['initial_number_of_people'] = int(initial_number_of_people)
    setup['initial_number_of_houses'] = int(initial_number_of_houses)
    setup['minimum_free_houses_policy'] = int(minimum_free_houses_policy)
    setup['number_of_months_to_run'] = int(number_of_months_to_run)
    setup['average_house_cost'] = float(average_house_cost)
    setup['sigma_house_cost'] = float(sigma_house_cost)
    setup['number_of_shares_per_house'] = int(number_of_shares_per_house)

    stats = run(setup=setup, verbose=False)
    human, money = get_general_figures(stats)
    house_timeline = get_house_timeline(stats)
    people_timeline = get_people_timeline(stats, allow_inheritance, ruleset)
    return human, money, house_timeline, people_timeline, ''


app.layout = html.Div(children=[

    markdown('''
# Housing by shares simulation

Explanation at: https://github.com/cristianvasquez/housing


I don't have a finished idea of how this would work, so I programmed a simple simulation that spans for 300 years, in a micro community of people.
People can have childs and die, and wants to give the *Housing by shares* a try.

Since this is only a preliminary exploration, I try to keep it simple, for example,there are no taxes.

# Parameters

Initial values:

- The number of shares per house defaults to the number of months an average person can live. 
- The price of each share is: house cost/number of shares

I'm exploring two options, with inheritance and without, to see how it goes. If inheritance is enabled, a random sibling inherits the shares, otherwise the founder.
***
Explore the parameters below.
***
'''),

    html.Div([

        html.Div([
            html.Label('max people'),
            dcc.Input(id='max_people', value='{}'.format(DEFAULT_SETUP['max_people']), type='text'),
        ]),

        html.Div([
            html.Label('min people'),
            dcc.Input(id='min_people', value='{}'.format(DEFAULT_SETUP['min_people']), type='text'),
        ]),

        html.Div([
            html.Label('initial number of people'),
            dcc.Input(id='initial_number_of_people', value='{}'.format(DEFAULT_SETUP['initial_number_of_people']),
                      type='text'),
        ]),

        html.Div([
            html.Label('initial number of houses'),
            dcc.Input(id='initial_number_of_houses', value='{}'.format(DEFAULT_SETUP['initial_number_of_houses']),
                      type='text'),
        ]),

        html.Div([
            html.Label('minimum available houses (policy)'),
            dcc.Input(id='minimum_free_houses_policy', value='{}'.format(DEFAULT_SETUP['minimum_free_houses_policy']),
                      type='text'),
        ]),

        html.Div([
            html.Label('number of months to run (simulation)'),
            dcc.Input(id='number_of_months_to_run', value='{}'.format(DEFAULT_SETUP['number_of_months_to_run']),
                      type='text'),
        ]),

        html.Div([
            html.Label('average house cost'),
            dcc.Input(id='average_house_cost', value='{}'.format(DEFAULT_SETUP['average_house_cost']), type='text'),
        ]),

        html.Div([
            html.Label('house cost standard deviation'),
            dcc.Input(id='sigma_house_cost', value='{}'.format(DEFAULT_SETUP['sigma_house_cost']), type='text'),
        ]),

        html.Div([
            html.Label('number of shares per house'),
            dcc.Input(id='number_of_shares_per_house', value='{}'.format(DEFAULT_SETUP['number_of_shares_per_house']),
                      type='text'),
        ]),

        dcc.RadioItems(
            options=[
                {'label': 'Without inheritance', 'value': '1'},
                {'label': 'With inheritance', 'value': '2'},
            ],
            value='1',
            id='inheritance'
        ),

        dcc.RadioItems(
            options=[
                {'label': 'Housing by shares', 'value': '1'},
                {'label': 'Classical rent', 'value': '2'},
            ],
            value='1',
            id='ruleset'
        ),
        html.Button(id='submit-button-state', n_clicks=0, children='Run simulation'),
        dcc.Loading(
            id="loading-1",
            type="default",
            fullscreen=True,
            children=html.Div(id="loading-output-1")
        ),
    ], style={'columnCount': 6}),

    markdown('''
***
##  People and houses
'''),

    html.Div([
        dcc.Graph(id='human', figure=human)
    ]),

    markdown('''
***
##  Evolution of shares (House 0)
'''),

    dcc.Graph(
        id='house_timeline',
        figure=house_timeline
    ),

    markdown('''
***
# Founder's policy
'''),

    html.Div([
        dcc.Graph(id='money', figure=money)
    ]),

    markdown('''
***
# Wealth of the population
### Press the play button below
    the size of the bubble denotes income by shares.
'''),
    dcc.Graph(
        id='people_timeline',
        figure=people_timeline
    ),

])

if __name__ == '__main__':
    app.run_server(debug=False)

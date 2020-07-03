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
        State(component_id='number_of_shares_per_house', component_property='value'),
        State(component_id='house_to_rent_ratio', component_property='value'),
        State(component_id='shares_per_month_earnings', component_property='value'),
        State(component_id='average_salary', component_property='value'),
        State(component_id='sigma_salary', component_property='value'),
        State(component_id='retirement_factor', component_property='value')
    ]
)
def update(n_clicks, inheritance, ruleset, max_people, min_people, initial_number_of_people, initial_number_of_houses,
           minimum_free_houses_policy, number_of_months_to_run, average_house_cost, sigma_house_cost,
           number_of_shares_per_house, house_to_rent_ratio, shares_per_month_earnings, average_salary, sigma_salary,
           retirement_factor):
    ruleset = Ruleset.by_shares if ruleset == '1' else Ruleset.normal_rent
    allow_inheritance = False if inheritance == '1' else True

    setup = DEFAULT_SETUP.copy()

    setup['number_of_months_to_run'] = int(number_of_months_to_run)
    setup['max_people'] = int(max_people)
    setup['min_people'] = int(min_people)
    setup['initial_number_of_people'] = int(initial_number_of_people)
    setup['initial_number_of_houses'] = int(initial_number_of_houses)
    setup['allow_inheritance'] = allow_inheritance
    setup['ruleset'] = ruleset

    setup['minimum_free_houses_policy'] = int(minimum_free_houses_policy)

    setup['average_house_cost'] = float(average_house_cost)
    setup['sigma_house_cost'] = float(sigma_house_cost)
    setup['number_of_shares_per_house'] = float(number_of_shares_per_house)
    setup['house_to_rent_ratio'] = float(house_to_rent_ratio)
    setup['shares_per_month_earnings'] = float(shares_per_month_earnings)

    # People earnings
    setup['average_salary'] = float(average_salary)
    setup['sigma_salary'] = float(sigma_salary)
    setup['retirement_factor'] = float(retirement_factor)

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

Since this is only a preliminary exploration, I try to keep it simple, for example,there are no taxes. At some point I want to add realistic values (when I have them)

# Questions

What is a fair 'house to rent' ratio in this setup? 

    * rent_price = house_price * house_to_rent_ratio
    
What is a fair number of shares per house?

    *  Current default: number of months an average person can live divided by two. 
    
How many shares a person earns per month?

    * Current default: shares_per_month = 1

# Parameters

I'm exploring two options, with inheritance and without, to see how it goes. If inheritance is enabled, a random sibling inherits the shares, otherwise the founder.
***
Explore the parameters below.
***
'''),

    html.Div([

        html.Div([
            html.Label('number of months to run (simulation)'),
            dcc.Input(id='number_of_months_to_run', value='{}'.format(DEFAULT_SETUP['number_of_months_to_run']),
                      type='text'),
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
            html.Label('min people'),
            dcc.Input(id='min_people', value='{}'.format(DEFAULT_SETUP['min_people']), type='text'),
        ]),

        html.Div([
            html.Label('max people'),
            dcc.Input(id='max_people', value='{}'.format(DEFAULT_SETUP['max_people']), type='text'),
        ]),

        html.Div([
            html.Label('minimum available houses (policy)'),
            dcc.Input(id='minimum_free_houses_policy', value='{}'.format(DEFAULT_SETUP['minimum_free_houses_policy']),
                      type='text'),
        ]),

        html.Div([
            html.Label('average house cost'),
            dcc.Input(id='average_house_cost', value='{}'.format(DEFAULT_SETUP['average_house_cost']), type='text'),
        ]),

        html.Div([
            html.Label('sigma house cost'),
            dcc.Input(id='sigma_house_cost', value='{}'.format(DEFAULT_SETUP['sigma_house_cost']), type='text'),
        ]),

        html.Div([
            html.Label('house to rent ratio'),
            dcc.Input(id='house_to_rent_ratio', value='{}'.format(DEFAULT_SETUP['house_to_rent_ratio']),
                      type='text'),
        ]),


        html.Div([
            html.Label('average salary'),
            dcc.Input(id='average_salary', value='{}'.format(DEFAULT_SETUP['average_salary']), type='text'),
        ]),

        html.Div([
            html.Label('sigma salary'),
            dcc.Input(id='sigma_salary', value='{}'.format(DEFAULT_SETUP['sigma_salary']), type='text'),
        ]),

        html.Div([
            html.Label('Percentage earned when retired'),
            dcc.Input(id='retirement_factor', value='{}'.format(DEFAULT_SETUP['retirement_factor']), type='text'),
        ]),

        html.Div([
            html.Label('number of shares per house'),
            dcc.Input(id='number_of_shares_per_house',
                      value='{}'.format(DEFAULT_SETUP['number_of_shares_per_house']),
                      type='text'),
        ]),

        html.Div([
            html.Label('shares per month earnings'),
            dcc.Input(id='shares_per_month_earnings', value='{}'.format(DEFAULT_SETUP['shares_per_month_earnings']),
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
    ], style={'columnCount': 4}),

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
    the size of the bubble denotes number of shares.
'''),
    dcc.Graph(
        id='people_timeline',
        figure=people_timeline
    ),

])

if __name__ == '__main__':
    app.run_server(debug=False)

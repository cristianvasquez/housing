import plotly.express as px
from pandas import DataFrame

from simulator.simulation import Ruleset


def get_house_timeline(stats):
    df = DataFrame.from_dict(stats.example_house_stats, "index")
    fig = px.line(df, x="year", y="shares", color="name")
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    return fig


def get_people_timeline(stats, allow_inheritance, ruleset):
    df = DataFrame.from_dict(stats.people_stats, "index")

    hover_data = {
        'year': False,
        'id': True,
        'money': ':.2f',
        'shares': ':.2f',
        'age': ':.2f',
        'parent': True,
        'inherited': True,
        'current_house': True,
        'monthly_payment': ':.2f',
        'share_income': ':.2f',
        'work_income': ':.2f',
        'income': ':.2f',
    }

    fig = px.scatter(df,
                     x="age",
                     y="money",
                     animation_frame="year",
                     animation_group="id",
                     size="share_income" if ruleset == Ruleset.by_shares else None,
                     color="income",
                     hover_name="id",
                     facet_col="inherited" if allow_inheritance else None,
                     log_x=False,
                     size_max=45,
                     range_color=[df['income'].min(), df['income'].max()],
                     color_continuous_scale='Bluered_r',
                     range_x=[df['age'].min(), df['age'].max()],
                     range_y=[0, df['money'].max()],
                     hover_data=hover_data
                     )
    return fig

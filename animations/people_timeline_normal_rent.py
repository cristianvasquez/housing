import plotly.express as px
from pandas import DataFrame

from main import run
from simulation import Ruleset

stats = run(allow_inheritance=False, ruleset=Ruleset.normal_rent)
df = DataFrame.from_dict(stats.people_stats, "index")

hover_data = {
    'year': False,
    'id': True,
    'money': ':.2f',
    'shares': False,
    'age': ':.2f',
    'parent': True,
    'inherited': False,
    'current_house': True,
    'monthly_payment': ':.2f',
    'share_income': False,
    'work_income': ':.2f',
    'income': ':.2f',
}

fig = px.scatter(df,
                 x="age",
                 y="money",
                 animation_frame="year",
                 animation_group="id",
                 # size="share_income",
                 color="income",
                 hover_name="id",
                 log_x=False,
                 size_max=45,
                 range_color=[df['income'].min(), df['income'].max()],
                 color_continuous_scale='Bluered_r',
                 range_x=[df['age'].min(), df['age'].max()],
                 range_y=[0, df['money'].max()],
                 hover_data=hover_data)

fig.update_layout(
    title_text='Normal rent'
)

fig.show()

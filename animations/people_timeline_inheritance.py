import plotly.express as px
from pandas import DataFrame

from main import run

stats = run(allow_inheritance=True)
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
                 size="share_income",
                 color="income",
                 # color="shares",
                 hover_name="id",
                 facet_col="inherited",
                 log_x=False,
                 size_max=45,
                 range_color=[df['income'].min(), df['income'].max()],
                 color_continuous_scale='Bluered_r',
                 range_x=[df['age'].min(), df['age'].max()],
                 range_y=[0, df['money'].max()],
                 hover_data=hover_data
                 )

fig.update_layout(
    title_text='Share acquisition, with inheritance. Size denotes the income by shares'
)

# Perhaps is better share_income/age

# fig = px.scatter(df,
#                  x="age",
#                  y="share_income",
#                  animation_frame="year",
#                  animation_group="id",
#                  size="shares",
#                  # color="continent",
#                  color="money",
#                  hover_name="id",
#                  facet_col="inherited",
#                  log_x=False,
#                  size_max=45,
#                  range_x=[df['age'].min(), df['age'].max()],
#                  range_y=[0, df['share_income'].max()], )
fig.show()

import plotly.express as px
from pandas import DataFrame

from main import run

stats = run(inheritance=True)
df = DataFrame.from_dict(stats.people_stats, "index")

fig = px.scatter(df,
                 x="age",
                 y="money",
                 animation_frame="year",
                 animation_group="id",
                 size="share_income",
                 # color="continent",
                 color="shares",
                 hover_name="id",
                 facet_col="inherited",
                 log_x=False,
                 size_max=45,
                 range_color=[df['shares'].min(), df['shares'].max()],
                 range_x=[df['age'].min(), df['age'].max()],
                 range_y=[0, df['money'].max()], )

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

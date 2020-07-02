import plotly.express as px
from pandas import DataFrame

from main import run

stats = run(allow_inheritance=False)
df = DataFrame.from_dict(stats.general_stats, "index")

# 'year': year,
# 'homeless_people': len(self.homeless_people),
# 'houses': len(self.houses),
# 'alive': len(self.people),
# 'dead': len(self.dead_people),
# 'brother_state_money': self.founder.money,
# 'spent_building_houses': self.founder.spent_building_houses,

fig = px.line(df, x="year", y="brother_state_money", title="General statistics")
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x unified")

fig.show()
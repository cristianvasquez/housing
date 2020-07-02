from pandas import DataFrame
import plotly.express as px

from main import run

stats = run(allow_inheritance=True)
df = DataFrame.from_dict(stats.example_house_stats, "index")

fig = px.line(df, x="year", y="shares", color="name", title="Ownership of shares for House number 0")
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x unified")

fig.show()
import plotly.express as px

import plotly.graph_objects as go

fig = go.Figure(go.Treemap(
    labels=["Eve", "Cain", "Azura"],
    parents=["", "", "", ],
    values=[1, 2, 10, ],
))

fig.show()

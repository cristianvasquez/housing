import plotly.express as px
from pandas import DataFrame

def get_general_figures(stats):
    df = DataFrame.from_dict(stats.general_stats, "index")
    human_df = df.query("scale=='human'")

    human = px.line(human_df, x="year", y="amount", color='type')

    money_df = df.query("scale=='money'")

    money = px.line(money_df, x="year", y="amount", color='type')

    return human, money

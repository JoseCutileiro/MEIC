from pandas import read_csv, DataFrame, Series
from matplotlib.pyplot import figure, savefig, show
from dslabs_functions import plot_line_chart, HEIGHT
from dslabs_functions import plot_line_chart
from dslabs_functions import HEIGHT, ts_aggregation_by

"""
file_tag = "COVID"
filename = "data/forecast_covid_single.csv"
index = "date"
target = "deaths"
data: DataFrame = read_csv(
    filename,
    index_col=index,
    sep=",",
    decimal=".",
    parse_dates=True,
    infer_datetime_format=True,
)
series: Series = data[target]
ss_daily: Series = ts_aggregation_by(series, gran_level="D", agg_func=sum)
ss_smooth_25: Series = ss_daily.rolling(window=25).mean()

figure(figsize=(3 * HEIGHT, HEIGHT / 2))
plot_line_chart(
    ss_smooth_25.index.to_list(),
    ss_smooth_25.to_list(),
    xlabel=ss_smooth_25.index.name,
    ylabel=target,
    title=f"{file_tag} hourly {target}",
)
savefig(f"images/{file_tag}_differenciation.png")

ss_diff: Series = ss_smooth_25.diff()
figure(figsize=(3 * HEIGHT, HEIGHT))
plot_line_chart(
    ss_diff.index.to_list(),
    ss_diff.to_list(),
    title="Differentiation",
    xlabel=series.index.name,
    ylabel=target,
)
savefig(f"images/{file_tag}_Diff_differenciation.png")

ss_diff_diff: Series = ss_diff.diff()
figure(figsize=(3 * HEIGHT, HEIGHT))
plot_line_chart(
    ss_diff_diff.index.to_list(),
    ss_diff_diff.to_list(),
    title="Second differentiation",
    xlabel=series.index.name,
    ylabel=target,
)
savefig(f"images/{file_tag}_DiffDiff_differenciation.png")
"""

"""-----------------------------------------------------------------------------------"""
# check the variation of the series
file_tag = "CREDIT"
filename = "forecast_traffic_single.csv"
index = "Timestamp"
target = "Total"
data: DataFrame = read_csv(
    filename,
    index_col=index,
    sep=",",
    decimal=".",
    parse_dates=True,
    infer_datetime_format=True,
)
series: Series = data[target]
ss_minutely: Series = ts_aggregation_by(series, gran_level="T", agg_func=sum)
ss_smooth_25: Series = ss_minutely.rolling(window=100).mean()

figure(figsize=(3 * HEIGHT, HEIGHT / 2))
plot_line_chart(
    ss_smooth_25.index.to_list(),
    ss_smooth_25.to_list(),
    xlabel=ss_smooth_25.index.name,
    ylabel=target,
    title=f"{file_tag} hourly {target}",
)
savefig(f"images/{file_tag}_differenciation.png")

ss_diff: Series = ss_smooth_25.diff()
figure(figsize=(3 * HEIGHT, HEIGHT))
plot_line_chart(
    ss_diff.index.to_list(),
    ss_diff.to_list(),
    title="Differentiation",
    xlabel=series.index.name,
    ylabel=target,
)
savefig(f"images/{file_tag}_Diff_differenciation.png")

ss_diff_diff: Series = ss_diff.diff()
figure(figsize=(3 * HEIGHT, HEIGHT))
plot_line_chart(
    ss_diff_diff.index.to_list(),
    ss_diff_diff.to_list(),
    title="Second differentiation",
    xlabel=series.index.name,
    ylabel=target,
)
savefig(f"images/{file_tag}_DiffDiff_differenciation.png")
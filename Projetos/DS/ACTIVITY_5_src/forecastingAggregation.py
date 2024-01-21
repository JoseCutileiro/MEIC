from pandas import read_csv, DataFrame, Series
from matplotlib.pyplot import figure, savefig, show
from dslabs_functions import plot_line_chart, ts_aggregation_by, HEIGHT

file_tag = "COVID"
target = "deaths"
data: DataFrame = read_csv(
    "data/forecast_covid_single.csv",
    index_col="date",
    sep=",",
    decimal=".",
    parse_dates=True,
    infer_datetime_format=True,
)

series: Series = data[target]
ss_Daily: Series = ts_aggregation_by(series, gran_level="D", agg_func="sum")
figure(figsize=(3 * HEIGHT, HEIGHT / 2))
plot_line_chart(
    ss_Daily.index.to_list(),
    ss_Daily.to_list(),
    xlabel=ss_Daily.index.name,
    ylabel=target,
    title=f"{file_tag} daily {target}",
)
savefig(f"images/{file_tag}_forecastingDaily_{target}.png")

figure(figsize=(3 * HEIGHT, HEIGHT / 2))
ss_Monthly: Series = ts_aggregation_by(series, gran_level="M", agg_func="sum")
plot_line_chart(
    ss_Monthly.index.to_list(),
    ss_Monthly.to_list(),
    xlabel=ss_Monthly.index.name,
    ylabel=target,
    title=f"{file_tag} monhtly {target}",
)
savefig(f"images/{file_tag}_forecastingMonhtly_{target}.png")

figure(figsize=(3 * HEIGHT, HEIGHT / 2))
ss_Quarterly: Series = ts_aggregation_by(series, gran_level="Q", agg_func="sum")
plot_line_chart(
    ss_Quarterly.index.to_list(),
    ss_Quarterly.to_list(),
    xlabel=ss_Quarterly.index.name,
    ylabel=target,
    title=f"{file_tag} quarterly {target}",
)
savefig(f"images/{file_tag}_forecastingQuarterly_{target}.png")

"""------------------------------------------------------------------"""


file_tag = "CREDIT"
target = "Total"
data: DataFrame = read_csv(
    "data/forecast_traffic_single.csv",
    index_col="Timestamp",
    sep=",",
    decimal=".",
    parse_dates=True,
    infer_datetime_format=True,
)
series: Series = data[target]

figure(figsize=(3 * HEIGHT, HEIGHT / 2))
ss_Minutely: Series = ts_aggregation_by(series, gran_level="T", agg_func="sum")
plot_line_chart(
    ss_Minutely.index.to_list(),
    ss_Minutely.to_list(),
    xlabel=ss_Minutely.index.name,
    ylabel=target,
    title=f"{file_tag} minutely {target}",
)
savefig(f"images/{file_tag}_forecastingMinutely_{target}.png")

figure(figsize=(3 * HEIGHT, HEIGHT / 2))
ss_Hourly: Series = ts_aggregation_by(series, gran_level="H", agg_func="sum")
plot_line_chart(
    ss_Hourly.index.to_list(),
    ss_Hourly.to_list(),
    xlabel=ss_Hourly.index.name,
    ylabel=target,
    title=f"{file_tag} hourly {target}",
)
savefig(f"images/{file_tag}_forecastingHourly_{target}.png")

ss_Daily: Series = ts_aggregation_by(series, gran_level="D", agg_func="sum")
figure(figsize=(3 * HEIGHT, HEIGHT / 2))
plot_line_chart(
    ss_Daily.index.to_list(),
    ss_Daily.to_list(),
    xlabel=ss_Daily.index.name,
    ylabel=target,
    title=f"{file_tag} daily {target}",
)
savefig(f"images/{file_tag}_forecastingDaily_{target}.png")
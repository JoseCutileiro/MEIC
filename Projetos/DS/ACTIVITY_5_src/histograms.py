from numpy import sum
from pandas import DataFrame, Series, read_csv
from matplotlib.pyplot import savefig
from dslabs_functions import HEIGHT, ts_aggregation_by
from numpy import array
from matplotlib.pyplot import subplots
from matplotlib.figure import Figure
from dslabs_functions import set_chart_labels

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
ss_days: Series = ts_aggregation_by(series, gran_level="D", agg_func=sum)
ss_monthly: Series = ts_aggregation_by(series, gran_level="M", agg_func=sum)
ss_quarters: Series = ts_aggregation_by(series, gran_level="Q", agg_func=sum)

grans: list[Series] = [ss_days, ss_monthly, ss_quarters]
gran_names: list[str] = ["Daily", "Monthly", "Quarterly"]
fig: Figure
axs: array
fig, axs = subplots(1, len(grans), figsize=(len(grans) * HEIGHT, HEIGHT))
fig.suptitle(f"{file_tag} {target}")
for i in range(len(grans)):
    set_chart_labels(axs[i], title=f"{gran_names[i]}", xlabel=target, ylabel="Nr records")
    axs[i].hist(grans[i].values)
savefig(f"images/{file_tag}_histograms_{target}.png")


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
ss_minutes: Series = ts_aggregation_by(series, gran_level="T", agg_func=sum)
ss_hours: Series = ts_aggregation_by(series, gran_level="H", agg_func=sum)
ss_days: Series = ts_aggregation_by(series, gran_level="D", agg_func=sum)

grans: list[Series] = [ss_minutes, ss_hours, ss_days]
gran_names: list[str] = ["Minutely", "Hourly", "Daily"]
fig: Figure
axs: array
fig, axs = subplots(1, len(grans), figsize=(len(grans) * HEIGHT, HEIGHT))
fig.suptitle(f"{file_tag} {target}")
for i in range(len(grans)):
    set_chart_labels(axs[i], title=f"{gran_names[i]}", xlabel=target, ylabel="Nr records")
    axs[i].hist(grans[i].values)
savefig(f"images/{file_tag}_histograms_{target}.png")
from numpy import sum
from pandas import DataFrame, Series, read_csv
from matplotlib.pyplot import figure, show, savefig
from dslabs_functions import HEIGHT, plot_line_chart, ts_aggregation_by
from numpy import array
from matplotlib.pyplot import show, subplots
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
ss_quarterly: Series = ts_aggregation_by(series, gran_level="Q", agg_func=sum)


fig: Figure
axs: array

fig, axs = subplots(2, 3, figsize=(3 * HEIGHT, HEIGHT))
set_chart_labels(axs[0, 0], title="Daily")
axs[0, 0].boxplot(ss_days)
set_chart_labels(axs[0, 1], title="Montly")
axs[0, 1].boxplot(ss_monthly)
set_chart_labels(axs[0, 2], title="Quarterly")
axs[0, 2].boxplot(ss_quarterly)

axs[1, 0].grid(False)
axs[1, 0].set_axis_off()
axs[1, 0].text(0.2, 0, str(ss_days.describe()), fontsize="small")

axs[1, 1].grid(False)
axs[1, 1].set_axis_off()
axs[1, 1].text(0.2, 0, str(ss_monthly.describe()), fontsize="small")

axs[1, 2].grid(False)
axs[1, 2].set_axis_off()
axs[1, 2].text(0.2, 0, str(ss_quarterly.describe()), fontsize="small")

savefig(f"images/{file_tag}_boxplot_{target}.png")


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

fig: Figure
axs: array

fig, axs = subplots(2, 3, figsize=(3 * HEIGHT, HEIGHT))
set_chart_labels(axs[0, 0], title="Minutely")
axs[0, 0].boxplot(ss_days)
set_chart_labels(axs[0, 1], title="Hourly")
axs[0, 1].boxplot(ss_monthly)
set_chart_labels(axs[0, 2], title="Daily")
axs[0, 2].boxplot(ss_quarterly)

axs[1, 0].grid(False)
axs[1, 0].set_axis_off()
axs[1, 0].text(0.2, 0, str(ss_days.describe()), fontsize="small")

axs[1, 1].grid(False)
axs[1, 1].set_axis_off()
axs[1, 1].text(0.2, 0, str(ss_monthly.describe()), fontsize="small")

axs[1, 2].grid(False)
axs[1, 2].set_axis_off()
axs[1, 2].text(0.2, 0, str(ss_quarterly.describe()), fontsize="small")

savefig(f"images/{file_tag}_boxplot_{target}.png")
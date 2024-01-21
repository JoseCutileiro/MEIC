from pandas import Series
from matplotlib.pyplot import savefig, subplots, show, gca
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from statsmodels.tsa.seasonal import DecomposeResult, seasonal_decompose
from dslabs_functions import HEIGHT, set_chart_labels
from matplotlib.pyplot import plot, legend
from pandas import DataFrame, Series, read_csv
from matplotlib.pyplot import figure, show
from dslabs_functions import plot_line_chart, ts_aggregation_by


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

def plot_components(
    series: Series,
    title: str = "",
    x_label: str = "time",
    y_label: str = "",
) -> list[Axes]:
    decomposition: DecomposeResult = seasonal_decompose(series, model="add", period=12)
    components: dict = {
        "observed": series,
        "trend": decomposition.trend,
        "seasonal": decomposition.seasonal,
        "residual": decomposition.resid,
    }
    rows: int = len(components)
    fig: Figure
    axs: list[Axes]
    fig, axs = subplots(rows, 1, figsize=(3 * HEIGHT, rows * HEIGHT))
    fig.suptitle(f"{title}")
    i: int = 0
    for key in components:
        set_chart_labels(axs[i], title=key, xlabel=x_label, ylabel=y_label)
        axs[i].plot(components[key])
        i += 1
    return axs


plot_components(
    series,
    title=f"{file_tag} monthly {target}",
    x_label=series.index.name,
    y_label=target,
)
show()
savefig(f"images/{file_tag}_components_{target}.png")

ss_monthly: Series = ts_aggregation_by(series, gran_level="M", agg_func=sum)

n: int = len(ss_monthly)
BINS = 10
mean_line: list[float] = []

for i in range(BINS):
    segment: Series = ss_monthly[i * n // BINS : (i + 1) * n // BINS]
    mean_value: list[float] = [segment.mean()] * (n // BINS)
    mean_line += mean_value
mean_line += [mean_line[-1]] * (n - len(mean_line))

figure(figsize=(3 * HEIGHT, HEIGHT))
plot_line_chart(
    ss_monthly.index.to_list(),
    ss_monthly.to_list(),
    xlabel=ss_monthly.index.name,
    ylabel=target,
    title=f"{file_tag} stationary study",
    name="original",
    show_stdev=True,
)
n: int = len(ss_monthly)
plot(ss_monthly.index, mean_line, "r-", label="mean")
legend()
savefig(f"images/{file_tag}_stationaryStudy_{target}.png")


############################# Augmented Dickey-Fuller test #############################

from statsmodels.tsa.stattools import adfuller

def eval_stationarity(series: Series) -> bool:
    result = adfuller(series)
    print(f"ADF Statistic: {result[0]:.3f}")
    print(f"p-value: {result[1]:.3f}")
    print("Critical Values:")
    for key, value in result[4].items():
        print(f"\t{key}: {value:.3f}")
    return result[1] <= 0.05


print(f"The series {('is' if eval_stationarity(ss_monthly) else 'is not')} stationary")



"""-----------------------------------------------------------------------------------"""

file_tag = "CREDIT"
filename = "data/forecast_traffic_single.csv"
target = "Total"
index = "Timestamp"
data: DataFrame = read_csv(
    filename,
    index_col=index,
    sep=",",
    decimal=".",
    parse_dates=True,
    infer_datetime_format=True,
)
series: Series = data[target]

def plot_components(
    series: Series,
    title: str = "",
    x_label: str = "time",
    y_label: str = "",
) -> list[Axes]:
    decomposition: DecomposeResult = seasonal_decompose(series, model="add", period=31)
    components: dict = {
        "observed": series,
        "trend": decomposition.trend,
        "seasonal": decomposition.seasonal,
        "residual": decomposition.resid,
    }
    rows: int = len(components)
    fig: Figure
    axs: list[Axes]
    fig, axs = subplots(rows, 1, figsize=(3 * HEIGHT, rows * HEIGHT))
    fig.suptitle(f"{title}")
    i: int = 0
    for key in components:
        set_chart_labels(axs[i], title=key, xlabel=x_label, ylabel=y_label)
        axs[i].plot(components[key])
        i += 1
    return axs


plot_components(
    series,
    title=f"{file_tag} daily {target}",
    x_label=series.index.name,
    y_label=target,
)
show()
savefig(f"images/{file_tag}_components_{target}.png")

ss_daily: Series = ts_aggregation_by(series, gran_level="D", agg_func=sum)

n: int = len(ss_daily)
BINS = 10
mean_line: list[float] = []

for i in range(BINS):
    segment: Series = ss_daily[i * n // BINS : (i + 1) * n // BINS]
    mean_value: list[float] = [segment.mean()] * (n // BINS)
    mean_line += mean_value
mean_line += [mean_line[-1]] * (n - len(mean_line))

figure(figsize=(3 * HEIGHT, HEIGHT))
plot_line_chart(
    ss_daily.index.to_list(),
    ss_daily.to_list(),
    xlabel=ss_daily.index.name,
    ylabel=target,
    title=f"{file_tag} stationary study",
    name="original",
    show_stdev=True,
)
n: int = len(ss_daily)
plot(ss_daily.index, mean_line, "r-", label="mean")
legend()
savefig(f"images/{file_tag}_stationaryStudy_{target}.png")

############################# Augmented Dickey-Fuller test #############################
print(f"The series {('is' if eval_stationarity(ss_daily) else 'is not')} stationary")

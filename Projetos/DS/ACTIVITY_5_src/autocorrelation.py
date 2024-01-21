from dslabs_functions import plot_multiline_chart
from pandas import DataFrame, Series, read_csv
from matplotlib.pyplot import figure, savefig
from dslabs_functions import HEIGHT
from matplotlib.gridspec import GridSpec

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


def get_lagged_series(series: Series, max_lag: int, delta: int = 1):
    lagged_series: dict = {"original": series, "lag 1": series.shift(1)}
    for i in range(delta, max_lag + 1, delta):
        lagged_series[f"lag {i}"] = series.shift(i)
    return lagged_series


figure(figsize=(3 * HEIGHT, HEIGHT))
lags = get_lagged_series(series, 20, 10)
plot_multiline_chart(series.index.to_list(), lags, xlabel=index, ylabel=target)

savefig(f"images/{file_tag}_autocorrelation_lag_plots_{target}.png")


def autocorrelation_study(series: Series, max_lag: int, delta: int = 1):
    k: int = int(max_lag / delta)
    fig = figure(figsize=(4 * HEIGHT, 2 * HEIGHT), constrained_layout=True)
    gs = GridSpec(2, k, figure=fig)

    series_values: list = series.tolist()
    for i in range(1, k + 1):
        ax = fig.add_subplot(gs[0, i - 1])
        lag = i * delta
        ax.scatter(series.shift(lag).tolist(), series_values)
        ax.set_title("Autocorrelation: lag-plots")
        ax.set_xlabel(f"lag {lag}")
        ax.set_ylabel("original")
    ax = fig.add_subplot(gs[1, :])
    ax.acorr(series, maxlags=max_lag)
    ax.set_title("Autocorrelation: correlogram")
    ax.set_xlabel("Lags")
    return


autocorrelation_study(series, 10, 1)
savefig(f"images/{file_tag}_autocorrelation_correlogram_{target}.png")


"""--------------------------------------------------------------------------------------------"""


file_tag = "CREDIT"
target = "Total"
index = "Timestamp"
data: DataFrame = read_csv(
    "data/forecast_traffic_single.csv",
    index_col= index,
    sep=",",
    decimal=".",
    parse_dates=True,
    infer_datetime_format=True,
)
series: Series = data[target]

figure(figsize=(3 * HEIGHT, HEIGHT))
lags = get_lagged_series(series, 20, 10)
plot_multiline_chart(series.index.to_list(), lags, xlabel=index, ylabel=target)

savefig(f"images/{file_tag}_autocorrelation_lag_plots_{target}.png")

autocorrelation_study(series, 10, 1)
savefig(f"images/{file_tag}_autocorrelation_correlogram_{target}.png")

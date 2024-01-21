from pandas import read_csv, DataFrame, Series
from matplotlib.pyplot import figure, show,savefig
from dslabs_functions import plot_line_chart, HEIGHT

file_tag = "COVID"
target = "deaths"
data: DataFrame = read_csv(
    "forecast_covid_single.csv",
    index_col="date",
    sep=",",
    decimal=".",
    parse_dates=True,
    infer_datetime_format=True,
)
series: Series = data[target]

from pandas import Index, Period


def ts_aggregation_by(
    data: Series | DataFrame,
    gran_level: str = "D",
    agg_func: str = "mean",
) -> Series | DataFrame:
    df: Series | DataFrame = data.copy()
    index: Index[Period] = df.index.to_period(gran_level)
    print(index)
    df = df.groupby(by=index, dropna=True, sort=True).agg(agg_func)
    df.index.drop_duplicates()
    df.index = df.index.to_timestamp()

    return df
"""
def granularity_daily():
    ss_days: Series = ts_aggregation_by(series, "D")
    figure(figsize=(3 * HEIGHT, HEIGHT / 2))
    plot_line_chart(
        ss_days.index.to_list(),
        ss_days.to_list(),
        xlabel="days",
        ylabel=target,
        title=f"{file_tag} daily mean {target}",
    )

    savefig(f"images/{file_tag}_daily_mean_{target}.png")
    
def granularity_monthly():
    ss_days: Series = ts_aggregation_by(series, "M")
    figure(figsize=(3 * HEIGHT, HEIGHT / 2))
    plot_line_chart(
        ss_days.index.to_list(),
        ss_days.to_list(),
        xlabel="days",
        ylabel=target,
        title=f"{file_tag} monthly mean {target}",
    )

    savefig(f"images/{file_tag}_monthly_mean_{target}.png")
    
def granularity_quarterly():
    ss_days: Series = ts_aggregation_by(series, "Q")
    figure(figsize=(3 * HEIGHT, HEIGHT / 2))
    plot_line_chart(
        ss_days.index.to_list(),
        ss_days.to_list(),
        xlabel="days",
        ylabel=target,
        title=f"{file_tag} quarterly mean {target}",
    )

    savefig(f"images/{file_tag}_quarterly_mean_{target}.png")
    
granularity_daily()
granularity_monthly()
granularity_quarterly()
"""

file_tag = "CREDIT"
target = "Total"
data: DataFrame = read_csv(
    "forecast_traffic_single.csv",
    index_col="Timestamp",
    sep=",",
    decimal=".",
    parse_dates=True,
    infer_datetime_format=True,
)
series: Series = data[target]

def granularity_daily():
    ss_days: Series = ts_aggregation_by(series, "D")
    figure(figsize=(3 * HEIGHT, HEIGHT / 2))
    plot_line_chart(
        ss_days.index.to_list(),
        ss_days.to_list(),
        xlabel="days",
        ylabel=target,
        title=f"{file_tag} daily mean {target}",
    )

    savefig(f"images/{file_tag}_daily_mean_{target}.png")

def granularity_minutely():
    ss_days: Series = ts_aggregation_by(series, "T")
    figure(figsize=(3 * HEIGHT, HEIGHT / 2))
    plot_line_chart(
        ss_days.index.to_list(),
        ss_days.to_list(),
        xlabel="minutes",
        ylabel=target,
        title=f"{file_tag} minutely mean {target}",
    )

    savefig(f"images/{file_tag}_minutely_mean_{target}.png")

def granularity_hourly():
    ss_days: Series = ts_aggregation_by(series, "H")
    figure(figsize=(3 * HEIGHT, HEIGHT / 2))
    plot_line_chart(
        ss_days.index.to_list(),
        ss_days.to_list(),
        xlabel="hours",
        ylabel=target,
        title=f"{file_tag} hourly mean {target}",
    )

    savefig(f"images/{file_tag}_hourly_mean_{target}.png")
    
granularity_minutely()
granularity_hourly()
granularity_daily()
    

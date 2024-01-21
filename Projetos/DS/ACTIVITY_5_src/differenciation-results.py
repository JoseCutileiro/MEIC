from numpy import arange, nan_to_num
from pandas import read_csv, DataFrame, Series
from matplotlib.pyplot import savefig
from sklearn.linear_model import LinearRegression
from dslabs_functions import HEIGHT, ts_aggregation_by, plot_forecasting_series
from matplotlib.axes import Axes
from matplotlib.pyplot import subplots, savefig
from dslabs_functions import PAST_COLOR, FUTURE_COLOR, PRED_PAST_COLOR, PRED_FUTURE_COLOR, HEIGHT, plot_multibar_chart, FORECAST_MEASURES
from math import sqrt

def series_train_test_split(data: Series, trn_pct: float = 0.90) -> tuple[Series, Series]:
    trn_size: int = int(len(data) * trn_pct)
    train: Series = data.iloc[:trn_size]
    test: Series = data.iloc[trn_size:]
    return train, test


def plot_forecasting_series(
    trn: Series,
    tst: Series,
    prd_tst: Series,
    title: str = "",
    xlabel: str = "time",
    ylabel: str = "",
) -> list[Axes]:
    fig, ax = subplots(1, 1, figsize=(4 * HEIGHT, HEIGHT), squeeze=True)
    fig.suptitle(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot(trn.index, trn.values, label="train", color=PAST_COLOR)
    ax.plot(tst.index, tst.values, label="test", color=FUTURE_COLOR)
    ax.plot(prd_tst.index, prd_tst.values, "--", label="test prediction", color=PRED_FUTURE_COLOR)
    ax.legend(prop={"size": 5})

    return ax


def plot_forecasting_eval(trn: Series, tst: Series, prd_trn: Series, prd_tst: Series, title: str = "") -> list[Axes]:
    # NaN values
    
    fill_value = 0  # Choose an appropriate fill value
    trn = trn.fillna(fill_value)
    tst = tst.fillna(fill_value)
    prd_trn = prd_trn.fillna(fill_value)
    prd_tst = prd_tst.fillna(fill_value)

    ev1: dict = {
        "RMSE": [sqrt(FORECAST_MEASURES["MSE"](trn, prd_trn)), sqrt(FORECAST_MEASURES["MSE"](tst, prd_tst))],
        "MAE": [FORECAST_MEASURES["MAE"](trn, prd_trn), FORECAST_MEASURES["MAE"](tst, prd_tst)],
    }
    ev2: dict = {
        "MAPE": [FORECAST_MEASURES["MAPE"](trn, prd_trn), FORECAST_MEASURES["MAPE"](tst, prd_tst)],
        "R2": [FORECAST_MEASURES["R2"](trn, prd_trn), FORECAST_MEASURES["R2"](tst, prd_tst)],
    }

    # print(eval1, eval2)
    fig, axs = subplots(1, 2, figsize=(1.5 * HEIGHT, 0.75 * HEIGHT), squeeze=True)
    fig.suptitle(title)
    plot_multibar_chart(["train", "test"], ev1, ax=axs[0], title="Scale-dependent error", percentage=False)
    plot_multibar_chart(["train", "test"], ev2, ax=axs[1], title="Percentage error", percentage=True)
    return axs


def compute_results(train, test, differencing):
    trnX = arange(len(train)).reshape(-1, 1)
    trnY = train.to_numpy()
    tstX = arange(len(train), len(train) + len(test)).reshape(-1, 1)
    tstY = test.to_numpy()

    # Handle NaN values using nan_to_num
    trnY = nan_to_num(trnY, nan=0)
    tstY = nan_to_num(tstY, nan=0)

    model = LinearRegression()
    model.fit(trnX, trnY)

    prd_trn: Series = Series(model.predict(trnX), index=train.index)
    prd_tst: Series = Series(model.predict(tstX), index=test.index)

    plot_forecasting_eval(train, test, prd_trn, prd_tst, title=f"{file_tag} - Linear Regression")
    savefig(f"images/{file_tag}_linear_regression_eval_{differencing}.png")

    plot_forecasting_series(
        train,
        test,
        prd_tst,
        title=f"{file_tag} - Linear Regression",
        xlabel=timecol,
        ylabel=target,
    )
    savefig(f"images/{file_tag}_linear_regression_forecast_{differencing}.png")

differencing_levels = ["original", "first_derivative", "second_derivative"]

"----------------------------------------------------------------------------------------------------"

filename: str = "data/forecast_covid_single.csv"
file_tag: str = "COVID"
target: str = "deaths"
timecol: str = "date"

data: DataFrame = read_csv(filename, index_col=timecol, sep=",", decimal=".", parse_dates=True)
series: Series = data[target]
ss_daily: Series = ts_aggregation_by(series, gran_level="D", agg_func=sum)
ss_smooth_50: Series = ss_daily.rolling(window=50).mean()
ss_diff: Series = ss_smooth_50.diff()
ss_diff_diff: Series = ss_diff.diff()

train_smooth_50, test_smooth_50 = series_train_test_split(ss_smooth_50, trn_pct=0.70)
train_diff, test_diff = series_train_test_split(ss_diff, trn_pct=0.70)
train_diff_diff, test_diff_diff = series_train_test_split(ss_diff_diff, trn_pct=0.70)

compute_results(train_smooth_50, test_smooth_50, differencing_levels[0])
compute_results(train_diff, test_diff, differencing_levels[1])
compute_results(train_diff_diff, test_diff_diff, differencing_levels[2])

# Chosen: 

"-----------------------------------------------------------------------------------"

filename: str = "forecast_traffic_single.csv"
file_tag: str = "CREDIT"
target: str = "Total"
timecol: str = "Timestamp"

data: DataFrame = read_csv(filename, index_col=timecol, sep=",", decimal=".", parse_dates=True)
series: Series = data[target]
ss_minutely: Series = ts_aggregation_by(series, gran_level="T", agg_func=sum)
ss_smooth_25: Series = ss_minutely.rolling(window=25).mean()
ss_diff: Series = ss_smooth_25.diff()
ss_diff_diff: Series = ss_diff.diff()

train_smooth_25, test_smooth_25 = series_train_test_split(ss_smooth_25, trn_pct=0.70)
train_diff, test_diff = series_train_test_split(ss_diff, trn_pct=0.70)
train_diff_diff, test_diff_diff = series_train_test_split(ss_diff_diff, trn_pct=0.70)

compute_results(train_smooth_25, test_smooth_25, differencing_levels[0])
compute_results(train_diff, test_diff, differencing_levels[1])
compute_results(train_diff_diff, test_diff_diff, differencing_levels[2])

# Chosen: 
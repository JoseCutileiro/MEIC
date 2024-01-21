from pandas import Series, read_csv, DataFrame
from matplotlib.axes import Axes
from matplotlib.pyplot import subplots, savefig
from dslabs_functions import PAST_COLOR, FUTURE_COLOR, PRED_PAST_COLOR, PRED_FUTURE_COLOR, HEIGHT, plot_multibar_chart, FORECAST_MEASURES
from math import sqrt
from sklearn.base import RegressorMixin
from dslabs_functions import HEIGHT, ts_aggregation_by

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


class SimpleAvgRegressor(RegressorMixin):
    def __init__(self):
        super().__init__()
        self.mean: float = 0.0
        return

    def fit(self, X: Series):
        self.mean = X.mean()
        return

    def predict(self, X: Series) -> Series:
        prd: list = len(X) * [self.mean]
        prd_series: Series = Series(prd)
        prd_series.index = X.index
        return prd_series
    
################################## COVID ##################################

filename: str = "forecast_covid_single.csv"
file_tag: str = "COVID"
target: str = "deaths"
timecol: str = "date"

data: DataFrame = read_csv(filename, index_col=timecol, sep=",", decimal=".", parse_dates=True)
series: Series = data[target]
ss_daily: Series = ts_aggregation_by(series, gran_level="D", agg_func=sum)
ss_smooth_50: Series = ss_daily.rolling(window=50).mean()

train_50, _ = series_train_test_split(ss_smooth_50, trn_pct=0.90)
_, test = series_train_test_split(ss_daily, trn_pct=0.90)

train_50_clean = train_50.fillna(train_50.mean())

fr_mod = SimpleAvgRegressor()
fr_mod.fit(train_50_clean)
prd_trn: Series = fr_mod.predict(train_50_clean)
prd_tst: Series = fr_mod.predict(test)


plot_forecasting_eval(train_50_clean, test, prd_trn, prd_tst, title=f"{file_tag} - Simple Average")
savefig(f"images/covid/week_6_extra/{file_tag}_simpleAvg_eval.png")

plot_forecasting_series(
    train_50_clean,
    test,
    prd_tst,
    title=f"{file_tag} - Simple Average",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/covid/week_6_extra/{file_tag}_simpleAvg_forecast.png")

################################## CREDIT SCORE ##################################

filename: str = "forecast_traffic_single.csv"
file_tag: str = "CREDIT"
target: str = "Total"
timecol: str = "Timestamp"

data: DataFrame = read_csv(filename, index_col=timecol, sep=",", decimal=".", parse_dates=True)
series: Series = data[target]
ss_minutes: Series = ts_aggregation_by(series, gran_level="T", agg_func=sum)
ss_smooth_25: Series = ss_minutes.rolling(window=25).mean()

train_25, _ = series_train_test_split(ss_smooth_25, trn_pct=0.90)
_, test = series_train_test_split(ss_minutes, trn_pct=0.90)

train_25_clean = train_25.fillna(train_25.mean())

fr_mod = SimpleAvgRegressor()
fr_mod.fit(train_25_clean)
prd_trn: Series = fr_mod.predict(train_25_clean)
prd_tst: Series = fr_mod.predict(test)

plot_forecasting_eval(train_25_clean, test, prd_trn, prd_tst, title=f"{file_tag} - Simple Average")
savefig(f"images/credit_score/week_6_extra/{file_tag}_simpleAvg_eval.png")

plot_forecasting_series(
    train_25_clean,
    test,
    prd_tst,
    title=f"{file_tag} - Simple Average",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/credit_score/week_6_extra/{file_tag}_simpleAvg_forecast.png")
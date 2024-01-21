from numpy import mean
from pandas import Series
from sklearn.base import RegressorMixin
from dslabs_functions import FORECAST_MEASURES, DELTA_IMPROVE, plot_line_chart
from pandas import read_csv, DataFrame
from matplotlib.pyplot import figure, savefig
from dslabs_functions import plot_forecasting_eval, plot_forecasting_series, HEIGHT,ts_aggregation_by

def series_train_test_split(data: Series, trn_pct: float = 0.90) -> tuple[Series, Series]:
    trn_size: int = int(len(data) * trn_pct)
    train: Series = data.iloc[:trn_size]
    test: Series = data.iloc[trn_size:]
    return train, test

class RollingMeanRegressor(RegressorMixin):
    def __init__(self, win: int = 3):
        super().__init__()
        self.win_size = win
        self.memory: list = []

    def fit(self, X: Series):
        self.memory = X.iloc[-self.win_size :]
        # print(self.memory)
        return

    def predict(self, X: Series):
        estimations = self.memory.tolist()
        for i in range(len(X)):
            new_value = mean(estimations[len(estimations) - self.win_size - i :])
            estimations.append(new_value)
        prd_series: Series = Series(estimations[-len(X):])
        prd_series.index = X.index
        return prd_series
    
def rolling_mean_study(train: Series, test: Series, measure: str = "R2"):
    # win_size = (3, 5, 10, 15, 20, 25, 30, 40, 50)
    win_size = (12, 24, 48, 96, 192, 384, 768)
    flag = measure == "R2" or measure == "MAPE"
    best_model = None
    best_params: dict = {"name": "Rolling Mean", "metric": measure, "params": ()}
    best_performance: float = -100000

    yvalues = []
    for w in win_size:
        pred = RollingMeanRegressor(win=w)
        pred.fit(train)
        prd_tst = pred.predict(test)

        eval: float = FORECAST_MEASURES[measure](test, prd_tst)
        # print(w, eval)
        if eval > best_performance and abs(eval - best_performance) > DELTA_IMPROVE:
            best_performance: float = eval
            best_params["params"] = (w,)
            best_model = pred
        yvalues.append(eval)

    print(f"Rolling Mean best with win={best_params['params'][0]:.0f} -> {measure}={best_performance}")
    plot_line_chart(
        win_size, yvalues, title=f"Rolling Mean ({measure})", xlabel="window size", ylabel=measure, percentage=flag
    )

    return best_model, best_params

################################## COVID ##################################

filename: str = "forecast_covid_single.csv"
file_tag: str = "COVID"
target: str = "deaths"
timecol: str = "date"
measure: str = "R2"

data: DataFrame = read_csv(filename, index_col=timecol, sep=",", decimal=".", parse_dates=True)
series: Series = data[target]
ss_daily: Series = ts_aggregation_by(series, gran_level="D", agg_func=sum)
ss_smooth_50: Series = ss_daily.rolling(window=50).mean()

train_50, _ = series_train_test_split(ss_smooth_50, trn_pct=0.90)
_, test = series_train_test_split(ss_daily, trn_pct=0.90)

train_50_clean = train_50.fillna(train_50.mean())

fig = figure(figsize=(HEIGHT, HEIGHT))
best_model, best_params = rolling_mean_study(train_50_clean, test)
savefig(f"images/covid/week_6_extra/{file_tag}_rollingmean_{measure}_study.png")

params = best_params["params"]
prd_trn: Series = best_model.predict(train_50_clean)
prd_tst: Series = best_model.predict(test)

plot_forecasting_eval(train_50_clean, test, prd_trn, prd_tst, title=f"{file_tag} - Rolling Mean (win={params[0]})")
savefig(f"images/covid/week_6_extra/{file_tag}_rollingmean_{measure}_win{params[0]}_eval.png")

plot_forecasting_series(
    train_50_clean,
    test,
    prd_tst,
    title=f"{file_tag} - Rolling Mean (win={params[0]})",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/covid/week_6_extra/{file_tag}_rollingmean_{measure}_forecast.png")

################################## CREDIT SCORE ##################################

filename: str = "forecast_traffic_single.csv"
file_tag: str = "CREDIT"
target: str = "Total"
timecol: str = "Timestamp"
measure: str = "R2"

data: DataFrame = read_csv(filename, index_col=timecol, sep=",", decimal=".", parse_dates=True)
series: Series = data[target]
ss_minutes: Series = ts_aggregation_by(series, gran_level="T", agg_func=sum)
ss_smooth_25: Series = ss_minutes.rolling(window=25).mean()

train_25, _ = series_train_test_split(ss_smooth_25, trn_pct=0.90)
_, test = series_train_test_split(ss_minutes, trn_pct=0.90)

train_25_clean = train_25.fillna(train_25.mean())

fig = figure(figsize=(HEIGHT, HEIGHT))
best_model, best_params = rolling_mean_study(train_25_clean, test)
savefig(f"images/credit_score/week_6_extra/{file_tag}_rollingmean_{measure}_study.png")

params = best_params["params"]
prd_trn: Series = best_model.predict(train_25_clean)
prd_tst: Series = best_model.predict(test)

plot_forecasting_eval(train_25_clean, test, prd_trn, prd_tst, title=f"{file_tag} - Rolling Mean (win={params[0]})")
savefig(f"images/credit_score/week_6_extra/{file_tag}_rollingmean_{measure}_win{params[0]}_eval.png")

plot_forecasting_series(
    train_25_clean,
    test,
    prd_tst,
    title=f"{file_tag} - Rolling Mean (win={params[0]})",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/credit_score/week_6_extra/{file_tag}_rollingmean_{measure}_forecast.png")


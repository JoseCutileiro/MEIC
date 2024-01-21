from pandas import Series
from sklearn.base import RegressorMixin
from pandas import read_csv, DataFrame, Series
from matplotlib.pyplot import savefig
from dslabs_functions import plot_forecasting_eval, plot_forecasting_series, ts_aggregation_by

def series_train_test_split(data: Series, trn_pct: float = 0.90) -> tuple[Series, Series]:
    trn_size: int = int(len(data) * trn_pct)
    train: Series = data.iloc[:trn_size]
    test: Series = data.iloc[trn_size:]
    return train, test


class PersistenceOptimistRegressor(RegressorMixin):
    def __init__(self):
        super().__init__()
        self.last: float = 0.0
        return

    def fit(self, X: Series):
        self.last = X.iloc[-1]
        # print(self.last)
        return

    def predict(self, X: Series):
        prd: list = X.shift().values.ravel()
        prd[0] = self.last
        prd_series: Series = Series(prd)
        prd_series.index = X.index
        return prd_series
    
class PersistenceRealistRegressor(RegressorMixin):
    def __init__(self):
        super().__init__()
        self.last = 0
        self.estimations = [0]
        self.obs_len = 0

    def fit(self, X: Series):
        for i in range(1, len(X)):
            self.estimations.append(X.iloc[i - 1])
        self.obs_len = len(self.estimations)
        self.last = X.iloc[len(X) - 1]
        prd_series: Series = Series(self.estimations)
        prd_series.index = X.index
        return prd_series

    def predict(self, X: Series):
        prd: list = len(X) * [self.last]
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

fr_mod = PersistenceOptimistRegressor()
fr_mod.fit(train_50_clean)
prd_trn: Series = fr_mod.predict(train_50_clean)
prd_tst: Series = fr_mod.predict(test)

plot_forecasting_eval(train_50_clean, test, prd_trn, prd_tst, title=f"{file_tag} - Persistence Optimist")
savefig(f"images/covid/week_6_extra/{file_tag}_persistence_optim_eval.png")

plot_forecasting_series(
    train_50_clean,
    test,
    prd_tst,
    title=f"{file_tag} - Persistence Optimist",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/covid/week_6_extra/{file_tag}_persistence_optim_forecast.png")

fr_mod = PersistenceRealistRegressor()
fr_mod.fit(train_50_clean)
prd_trn: Series = fr_mod.predict(train_50_clean)
prd_tst: Series = fr_mod.predict(test)

plot_forecasting_eval(train_50_clean, test, prd_trn, prd_tst, title=f"{file_tag} - Persistence Realist")
savefig(f"images/covid/week_6_extra/{file_tag}_persistence_real_eval.png")

plot_forecasting_series(
    train_50_clean,
    test,
    prd_tst,
    title=f"{file_tag} - Persistence Realist",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/covid/week_6_extra/{file_tag}_persistence_real_forecast.png")

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

fr_mod = PersistenceOptimistRegressor()
fr_mod.fit(train_25_clean)
prd_trn: Series = fr_mod.predict(train_25_clean)
prd_tst: Series = fr_mod.predict(test)

plot_forecasting_eval(train_25_clean, test, prd_trn, prd_tst, title=f"{file_tag} - Persistence Optimist")
savefig(f"images/credit_score/week_6_extra/{file_tag}_persistence_optim_eval.png")

plot_forecasting_series(
    train_25_clean,
    test,
    prd_tst,
    title=f"{file_tag} - Persistence Optimist",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/credit_score/week_6_extra/{file_tag}_persistence_optim_forecast.png")

fr_mod = PersistenceRealistRegressor()
fr_mod.fit(train_25_clean)
prd_trn: Series = fr_mod.predict(train_25_clean)
prd_tst: Series = fr_mod.predict(test)

plot_forecasting_eval(train_25_clean, test, prd_trn, prd_tst, title=f"{file_tag} - Persistence Realist")
savefig(f"images/credit_score/week_6_extra/{file_tag}_persistence_real_eval.png")

plot_forecasting_series(
    train_25_clean,
    test,
    prd_tst,
    title=f"{file_tag} - Persistence Realist",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/credit_score/week_6_extra/{file_tag}_persistence_real_forecast.png")

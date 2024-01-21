import warnings
from matplotlib.pylab import LinAlgError
from matplotlib.pyplot import savefig, show
from pandas import read_csv, DataFrame, Series
from sklearn.exceptions import ConvergenceWarning
from statsmodels.tsa.arima.model import ARIMA
from dslabs_functions import HEIGHT, ts_aggregation_by
from matplotlib.pyplot import figure, savefig, subplots
from dslabs_functions import FORECAST_MEASURES, DELTA_IMPROVE, plot_multiline_chart
from dslabs_functions import plot_forecasting_eval
from dslabs_functions import plot_forecasting_series

def series_train_test_split(data: Series, trn_pct: float = 0.90) -> tuple[Series, Series]:
    trn_size: int = int(len(data) * trn_pct)
    train: Series = data.iloc[:trn_size]
    test: Series = data.iloc[trn_size:]
    return train, test


def arima_study(train: Series, test: Series, measure: str = "R2"):
    d_values = (0, 1, 2)
    p_params = (1, 2, 3, 5, 7, 10)
    q_params = (1, 3, 5, 7)

    flag = measure == "R2" or measure == "MAPE"
    best_model = None
    best_params: dict = {"name": "ARIMA", "metric": measure, "params": ()}
    best_performance: float = -100000

    fig, axs = subplots(1, len(d_values), figsize=(len(d_values) * HEIGHT, HEIGHT))
    for i in range(len(d_values)):
        d: int = d_values[i]
        values = {}
        for q in q_params:
            yvalues = []
            for p in p_params:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore', ConvergenceWarning)
                        arima = ARIMA(train, order=(p, d, q))
                        model = arima.fit()
                except (ValueError, LinAlgError):  # Add except clause here
                    print(f"Model fitting failed for ARIMA({p}, {d}, {q})")
                    yvalues.append(None)  # Or some indicator of failure
                else:  # Add else clause here
                    prd_tst = model.forecast(steps=len(test), signal_only=False)
                    eval: float = FORECAST_MEASURES[measure](test, prd_tst)
                    # print(f"ARIMA ({p}, {d}, {q})", eval)
                    if eval > best_performance and abs(eval - best_performance) > DELTA_IMPROVE:
                        best_performance: float = eval
                        best_params["params"] = (p, d, q)
                        best_model = model
                    yvalues.append(eval)
                        
            values[q] = yvalues
        plot_multiline_chart(
            p_params, values, ax=axs[i], title=f"ARIMA d={d} ({measure})", xlabel="p", ylabel=measure, percentage=flag
        )
    print(
        f"ARIMA best results achieved with (p,d,q)=({best_params['params'][0]:.0f}, {best_params['params'][1]:.0f}, {best_params['params'][2]:.0f}) ==> measure={best_performance:.2f}"
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

predictor = ARIMA(train_50_clean, order=(3, 1, 2))
model = predictor.fit()
print(model.summary())

model.plot_diagnostics(figsize=(2 * HEIGHT, 1.5 * HEIGHT))
savefig(f"images/covid/week_6_extra/{file_tag}_arima_{measure}_diagnostics.png")

best_model, best_params = arima_study(train_50_clean, test, measure=measure)
savefig(f"images/covid/week_6_extra/{file_tag}_arima_{measure}_study.png")

params = best_params["params"]
prd_trn = best_model.predict(start=0, end=len(train_50_clean) - 1)
prd_tst = best_model.forecast(steps=len(test))

plot_forecasting_eval(
    train_50_clean, test, prd_trn, prd_tst, title=f"{file_tag} - ARIMA (p={params[0]}, d={params[1]}, q={params[2]})"
)
savefig(f"images/covid/week_6_extra/{file_tag}_arima_{measure}_eval.png")


plot_forecasting_series(
    train_50_clean,
    test,
    prd_tst,
    title=f"{file_tag} - ARIMA ",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/covid/week_6_extra/{file_tag}_arima_{measure}_forecast.png")

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

predictor = ARIMA(train_25_clean, order=(3, 1, 2))
model = predictor.fit()
print(model.summary())

model.plot_diagnostics(figsize=(2 * HEIGHT, 1.5 * HEIGHT))
savefig(f"images/credit_score/week_6_extra/{file_tag}_arima_{measure}_diagnostics.png")

best_model, best_params = arima_study(train_25_clean, test, measure=measure)
savefig(f"images/credit_score/week_6_extra/{file_tag}_arima_{measure}_study.png")

params = best_params["params"]
prd_trn = best_model.predict(start=0, end=len(train_25_clean) - 1)
prd_tst = best_model.forecast(steps=len(test))

plot_forecasting_eval(
    train_25_clean, test, prd_trn, prd_tst, title=f"{file_tag} - ARIMA (p={params[0]}, d={params[1]}, q={params[2]})"
)
savefig(f"images/credit_score/week_6_extra/{file_tag}_arima_{measure}_eval.png")


plot_forecasting_series(
    train_25_clean,
    test,
    prd_tst,
    title=f"{file_tag} - ARIMA ",
    xlabel=timecol,
    ylabel=target,
)
savefig(f"images/credit_score/week_6_extra/{file_tag}_arima_{measure}_forecast.png")
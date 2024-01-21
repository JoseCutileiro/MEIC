from pandas import DataFrame, read_csv, Series
from numpy import ndarray, log
from scipy.stats import norm, expon, lognorm
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.pyplot import savefig, show, subplots, figure
from dslabs_functions import define_grid, HEIGHT, set_chart_labels, get_variable_types, plot_multibar_chart, plot_multiline_chart, plot_bar_chart

file_tag = "health"
data: DataFrame = read_csv("class_pos_covid.csv", na_values="")

target = "CovidPos"

values: Series = data[target].value_counts()
print(values)

figure(figsize=(4, 2))
plot_bar_chart(
    values.index.to_list(),
    values.to_list(),
    title=f"Target distribution (target={target})",
)
savefig(f"images/{file_tag}_class_distribution.png")
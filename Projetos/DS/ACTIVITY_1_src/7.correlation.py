from pandas import read_csv, DataFrame
from matplotlib.pyplot import figure, savefig, show
from dslabs_functions import HEIGHT
from seaborn import heatmap
from dslabs_functions import get_variable_types

files = ["data/class_pos_covid.csv","data/class_credit_score.csv"]

for i in range(2):
    filename = files[i]
    file_tag = "SET_" + str(i + 1)
    data: DataFrame = read_csv(filename, na_values="")
    data = data.dropna()

    variables_types: dict[str, list] = get_variable_types(data)
    numeric: list[str] = variables_types["numeric"]
    corr_mtx: DataFrame = data[numeric].corr().abs()

    figure(figsize=(20, 10))
    heatmap(
        abs(corr_mtx),
        xticklabels=numeric,
        yticklabels=numeric,
        annot=False,
        cmap="Blues",
        vmin=0,
        vmax=1,
    )
    savefig(f"images/{file_tag}_correlation_analysis.png")
    show()
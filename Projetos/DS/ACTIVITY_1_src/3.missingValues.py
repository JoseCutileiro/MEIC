from matplotlib.pyplot import figure, savefig, show
from dslabs_functions import plot_bar_chart
from pandas import read_csv, DataFrame

files = ["data/class_pos_covid.csv","data/class_credit_score.csv"]

files = ["data/class_pos_covid.csv","data/class_credit_score.csv"]

for i in range(2):
    filename = files[i]
    file_tag = "SET_" + str(i + 1)

    data: DataFrame = read_csv(filename, na_values="")

    data.shape


    mv: dict[str, int] = {}
    for var in data.columns:
        nr: int = data[var].isna().sum()
        if nr > 0:
            mv[var] = nr

    figure(figsize=(15, 7.5))
    plot_bar_chart(
        list(mv.keys()),
        list(mv.values()),
        title="Nr of missing values per variable",
        xlabel="variables",
        ylabel="nr missing values",
    )
    savefig(f"images/{file_tag}_missing_values.png")
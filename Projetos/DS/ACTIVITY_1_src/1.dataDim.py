from pandas import read_csv, DataFrame
from matplotlib.pyplot import figure, savefig, show
from dslabs_functions import plot_bar_chart

files = ["data/class_pos_covid.csv","data/class_credit_score.csv"]

for i in range(2):
    filename = files[i]
    file_tag = "SET_" + str(i + 1)
    data: DataFrame = read_csv(filename, na_values="")

    data.shape

    figure(figsize=(8, 4))
    values: dict[str, int] = {"nr records": data.shape[0], "nr variables": data.shape[1]}
    plot_bar_chart(
        list(values.keys()), list(values.values()), title="Nr of records vs nr variables"
    )
    savefig(f"images/{file_tag}_records_variables.png")
    #show()
from numpy import ndarray
from pandas import read_csv, DataFrame
from matplotlib.figure import Figure
from matplotlib.pyplot import figure, subplots, savefig, show
from dslabs_functions import HEIGHT, plot_multi_scatters_chart

files = ["data/class_pos_covid.csv","data/class_credit_score.csv"]

for i in range(2):
    filename = files[i]
    file_tag = "SET_" + str(i + 1)
    data: DataFrame = read_csv(filename, na_values="")
    data = data.dropna()
    vars: list = data.columns.to_list()
    if [] != vars:
        target = "stroke"

        n: int = len(vars) - 1
        fig: Figure
        axs: ndarray
        fig, axs = subplots(n, n, figsize=(n * HEIGHT, n * HEIGHT), squeeze=False)
        for i in range(len(vars)):
            print(i)
            var1: str = vars[i]
            for j in range(i + 1, len(vars)):
                print(j)
                var2: str = vars[j]
                plot_multi_scatters_chart(data, var1, var2, ax=axs[i, j - 1])
        savefig(f"images/{file_tag}_sparsity_study.png")
        #show()
    else:
        print("Sparsity class: there are no variables.")
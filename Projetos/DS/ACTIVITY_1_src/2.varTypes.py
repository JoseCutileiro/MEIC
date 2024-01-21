from pandas import read_csv, DataFrame, Series, to_numeric, to_datetime
from matplotlib.pyplot import figure, savefig, show
from dslabs_functions import plot_bar_chart

def get_variable_types(df: DataFrame) -> dict[str, list]:
    variable_types: dict = {"numeric": [], "binary": [], "date": [], "symbolic": []}

    nr_values: Series = df.nunique(axis=0, dropna=True)
    for c in df.columns:
        if 2 == nr_values[c]:
            variable_types["binary"].append(c)
            df[c].astype("bool")
        else:
            try:
                to_numeric(df[c], errors="raise")
                variable_types["numeric"].append(c)
            except ValueError:
                try:
                    df[c] = to_datetime(df[c], errors="raise")
                    variable_types["date"].append(c)
                except ValueError:
                    variable_types["symbolic"].append(c)

    return variable_types

files = ["data/class_pos_covid.csv","data/class_credit_score.csv"]

for i in range(2):

    filename = files[i]
    file_tag = "SET_" + str(i + 1)
    data: DataFrame = read_csv(filename, na_values="")

    data.shape

    variable_types: dict[str, list] = get_variable_types(data)
    print(variable_types)
    counts: dict[str, int] = {}
    for tp in variable_types.keys():
        counts[tp] = len(variable_types[tp])

    figure(figsize=(14, 7))
    plot_bar_chart(
        list(counts.keys()), list(counts.values()), title="Nr of variables per type"
    )
    savefig(f"images/{file_tag}_variable_types.png")
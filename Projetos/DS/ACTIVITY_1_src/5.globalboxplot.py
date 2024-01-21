from matplotlib.pyplot import savefig, show
from dslabs_functions import get_variable_types
from pandas import DataFrame, read_csv

file_tag = "stroke"
data: DataFrame = read_csv("class_pos_covid.csv", na_values="")
variables_types: dict[str, list] = get_variable_types(data)
numeric: list[str] = variables_types["numeric"]
if [] != numeric:
    data[numeric].boxplot(rot=45)
    savefig(f"images/{file_tag}_global_boxplot.png")
    show()
else:
    print("There are no numeric variables.")
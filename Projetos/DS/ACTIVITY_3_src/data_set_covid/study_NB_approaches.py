import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from matplotlib.pyplot import figure, savefig, show
from dslabs_functions import CLASS_EVAL_METRICS, DELTA_IMPROVE, plot_bar_chart, plot_evaluation_results


file_tag = "COVID"
target = "CovidPos"
data = pd.read_csv("MEAN_IMPUTATION_OVER_SAMPLING_COVID.csv")

# Load and prepare the dataset for classification
# Splitting data into train and test sets
trnX, tstX, trnY, tstY = train_test_split(
    data.drop(target, axis=1), data[target], train_size=0.7, stratify=data[target]
)

# Save the train and test sets to CSV files
trn_data = pd.concat([trnX, trnY], axis=1)
tst_data = pd.concat([tstX, tstY], axis=1)

trn_data.to_csv("covid_nb_train.csv", index=False)
tst_data.to_csv("covid_nb_test.csv", index=False)

labels: list = list(data[target].unique())
labels.sort()
print(f"Labels={labels}")

# Study and evaluate NB models
def naive_Bayes_study(trnX, trnY, tstX, tstY, metric="accuracy"):
    estimators = {"GaussianNB": GaussianNB(), "BernoulliNB": BernoulliNB()}

    xvalues = []
    yvalues = []
    best_model = None
    best_params = {"name": "", "metric": metric, "params": ()}
    best_performance = 0

    for clf in estimators:
        xvalues.append(clf)
        estimators[clf].fit(trnX, trnY)
        prdY = estimators[clf].predict(tstX)

        print(f"Score over Train: {estimators[clf].score(trnX, trnY):.3f}")
        print(f"Score over Test: {estimators[clf].score(tstX, tstY):.3f}")
        
        eval = CLASS_EVAL_METRICS[metric](tstY, prdY)

        if eval - best_performance > DELTA_IMPROVE:
            best_performance = eval
            best_params["name"] = clf
            best_params[metric] = eval
            best_model = estimators[clf]

        yvalues.append(eval)

    plot_bar_chart(
        xvalues,
        yvalues,
        title=f"Naive Bayes Models ({metric})",
        ylabel=metric,
        percentage=True,
    )

    return best_model, best_params

best_model, params = naive_Bayes_study(trnX, trnY, tstX, tstY)
print(best_model)
print(params)

prd_trn = best_model.predict(trnX)
prd_tst = best_model.predict(tstX)

figure()
best_model, params = naive_Bayes_study(trnX, trnY, tstX, tstY, "accuracy")
savefig(f"images/{file_tag}_nb_{"accuracy"}_study.png")
show()

figure()
best_model, params = naive_Bayes_study(trnX, trnY, tstX, tstY, "recall")
savefig(f"images/{file_tag}_nb_recall_study.png")
show()

figure()
plot_evaluation_results(params, trnY, prd_trn, tstY, prd_tst, labels)
savefig(f'images/{file_tag}_{params["name"]}_best_{params["metric"]}_eval.png')
show()


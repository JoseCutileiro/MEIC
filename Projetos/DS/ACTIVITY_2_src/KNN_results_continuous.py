import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix


# Load CSV files
data_original = pd.read_csv('data/MEAN_IMPUTATION_credit_score.csv')
data_imputed = pd.read_csv('data/MEAN_IMPUTATION_Z_SCORE.csv')

# Convert 'Credit_Score' to categorical if it's numeric or continuous
def discretize_credit_score(data):
    if pd.api.types.is_numeric_dtype(data['Credit_Score']):
        # Define bins or use pd.cut to create bins automatically
        # For example, let's divide into 3 equal-width bins
        bins = pd.cut(data['Credit_Score'], bins=3, labels=['Low', 'Medium', 'High'])
        data['Credit_Score'] = bins
    return data

data_original = discretize_credit_score(data_original)
data_imputed = discretize_credit_score(data_imputed)

# Ensure 'Credit_Score' is categorical
data_original['Credit_Score'] = data_original['Credit_Score'].astype('category')
data_imputed['Credit_Score'] = data_imputed['Credit_Score'].astype('category')

# Convert 'Credit_Score' to categorical if it's numeric
data_original['Credit_Score'] = data_original['Credit_Score'].astype('category')
data_imputed['Credit_Score'] = data_imputed['Credit_Score'].astype('category')

# Separate target variable
target_original = data_original['Credit_Score']
features_original = data_original.drop('Credit_Score', axis=1)

target_imputed = data_imputed['Credit_Score']
features_imputed = data_imputed.drop('Credit_Score', axis=1)

# Train-test split
X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(features_original, target_original, test_size=0.2, random_state=42)
X_train_imp, X_test_imp, y_train_imp, y_test_imp = train_test_split(features_imputed, target_imputed, test_size=0.2, random_state=42)

# KNN model
knn = KNeighborsClassifier()

# Fit model on original data
knn.fit(X_train_orig, y_train_orig)

# Make predictions on imputed data
y_pred_imp = knn.predict(X_test_imp)

# Calculate metrics
accuracy = accuracy_score(y_test_imp, y_pred_imp)
precision = precision_score(y_test_imp, y_pred_imp, average='weighted')
recall = recall_score(y_test_imp, y_pred_imp, average='weighted')
conf_matrix = confusion_matrix(y_test_imp, y_pred_imp)

# Print metrics
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")

# Plotting metrics
metrics_data = {'Metrics': ['Accuracy', 'Precision', 'Recall'],
                'Scores': [accuracy, precision, recall]}

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

sns.barplot(x='Metrics', y='Scores', data=metrics_data, ax=axes[0])
axes[0].set_title('Evaluation Metrics')
axes[0].set_ylim(0, 1)  # Set y-axis limit for better visualization

sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='d', ax=axes[1])
axes[1].set_title('Confusion Matrix')
axes[1].set_xlabel('Predicted Labels')
axes[1].set_ylabel('True Labels')

plt.tight_layout()

# Save combined plots as an image
plt.savefig('ZSCORE_SCALE_KNN.png')
plt.show()
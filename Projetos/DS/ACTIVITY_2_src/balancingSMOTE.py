import pandas as pd
from imblearn.over_sampling import SMOTE

# Load the CSV file into a DataFrame
file_path = 'data/MEAN_IMPUTATION_credit_score.csv'  # Replace 'your_file.csv' with your CSV file path
data = pd.read_csv(file_path)

# Assuming 'target_column' is the column containing the target variable you want to balance
target_column = 'Credit_Score'  # Replace 'target_column' with your target column name

# Separate features and target variable
X = data.drop(columns=[target_column])
y = data[target_column]

# Instantiate SMOTE for oversampling
smote = SMOTE()

# Apply SMOTE to generate synthetic samples
X_resampled, y_resampled = smote.fit_resample(X, y)

# Create a new DataFrame with the resampled data
resampled_data = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name=target_column)], axis=1)

# Save the resampled data to a new CSV file
resampled_file_path = 'data/MEAN_IMPUTATION_SMOTE.csv'  # Replace 'smote_oversampled_file.csv' with your desired file path
resampled_data.to_csv(resampled_file_path, index=False)
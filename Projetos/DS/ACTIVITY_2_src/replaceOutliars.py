import pandas as pd
import numpy as np

# Load the CSV file into a pandas DataFrame
file_path = 'data/MEAN_IMPUTATION_credit_score.csv'  # Replace 'path_to_your_file.csv' with the actual file path
data = pd.read_csv(file_path)

# Function to replace outliers in any numeric column with a specified value (e.g., 0)
def replace_outliers_with_value(df, value=0, threshold=3):
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

    for column in numeric_columns:
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        df[column] = np.where(z_scores > threshold, value, df[column])

    return df

# Replace outliers in any numeric column with 0
cleaned_data = replace_outliers_with_value(data, value=0)

# Save the cleaned DataFrame to a new CSV file
cleaned_file_path = 'data/MEAN_IMPUTATION_REPLACE_OUTLIARS.csv'  # Replace with the desired file path
cleaned_data.to_csv(cleaned_file_path, index=False)
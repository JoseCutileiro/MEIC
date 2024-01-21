import pandas as pd
import numpy as np

# Load the CSV file into a pandas DataFrame
file_path = 'data/MEAN_IMPUTATION_credit_score.csv'  # Replace 'path_to_your_file.csv' with the actual file path
data = pd.read_csv(file_path)

# Function to identify and remove rows with outliers in any numeric column
def remove_outlier_rows(df, threshold=3):
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
    outlier_indices = set()

    for column in numeric_columns:
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        outlier_indices |= set(np.where(z_scores > threshold)[0])

    return df.drop(list(outlier_indices))

# Remove rows with outliers in any numeric column
cleaned_data = remove_outlier_rows(data)

# Save the cleaned DataFrame to a new CSV file
cleaned_file_path = 'data/MEAN_IMPUTATION_NO_OUTLIARS.csv'  # Replace with the desired file path
cleaned_data.to_csv(cleaned_file_path, index=False)
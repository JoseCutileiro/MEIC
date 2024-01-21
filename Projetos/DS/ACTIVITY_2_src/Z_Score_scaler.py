import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load the CSV file into a pandas DataFrame
file_path = 'data/MEAN_IMPUTATION_credit_score.csv'  # Replace 'path_to_your_file.csv' with the actual file path
data = pd.read_csv(file_path)

# Apply Z-score normalization to the numeric columns
scaler = StandardScaler()
numeric_columns = data.select_dtypes(include=np.number).columns.tolist()
data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

# Save the standardized DataFrame to a new CSV file
standardized_file_path = 'data/MEAN_IMPUTATION_Z_SCORE.csv'  # Replace with the desired file path
data.to_csv(standardized_file_path, index=False)
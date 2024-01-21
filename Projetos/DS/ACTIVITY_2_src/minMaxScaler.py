import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Load the CSV file into a pandas DataFrame
file_path = 'data/MEAN_IMPUTATION_credit_score.csv'  # Replace 'path_to_your_file.csv' with the actual file path
data = pd.read_csv(file_path)

# Apply Min-Max scaling to the numeric columns
scaler = MinMaxScaler()
numeric_columns = data.select_dtypes(include=np.number).columns.tolist()
data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

# Save the normalized DataFrame to a new CSV file
normalized_file_path = 'data/MEAN_IMPUTATION_MINMAX_SCALE.csv'  # Replace with the desired file path
data.to_csv(normalized_file_path, index=False)
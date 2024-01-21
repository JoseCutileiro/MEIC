import pandas as pd

# Read the CSV file
file_path = 'data/clean_class_credit_score.csv'  # Replace 'your_file_path.csv' with the path to your CSV file
data = pd.read_csv(file_path)

# Check for missing values
missing_values = data.isnull().sum()
print("Missing Values Before Imputation:")
print(missing_values)

# Perform mean imputation
data_filled_mean = data.fillna(data.mean())

# Check missing values after imputation
missing_values_after = data_filled_mean.isnull().sum()
print("\nMissing Values After Mean Imputation:")
print(missing_values_after)

# Save the imputed data to a new CSV file
output_file_path = 'data/MEAN_IMPUTATION_credit_score.csv'  # Replace 'imputed_data_mean.csv' with your desired output file path
data_filled_mean.to_csv(output_file_path, index=False)
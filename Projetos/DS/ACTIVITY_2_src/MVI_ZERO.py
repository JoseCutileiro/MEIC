import pandas as pd

# Read the CSV file
file_path = 'data/clean_class_credit_score.csv'  # Replace 'your_file_path.csv' with the path to your CSV file
data = pd.read_csv(file_path)

# Check for missing values
missing_values = data.isnull().sum()
print("Missing Values Before Imputation:")
print(missing_values)

# Perform constant (0) imputation
data_filled_constant = data.fillna(0)

# Check missing values after imputation
missing_values_after = data_filled_constant.isnull().sum()
print("\nMissing Values After Constant Imputation:")
print(missing_values_after)

# Save the imputed data to a new CSV file
output_file_path = 'data/ZERO_IMPUTATION_credit_score.csv'  # Replace 'imputed_data_constant.csv' with your desired output file path
data_filled_constant.to_csv(output_file_path, index=False)
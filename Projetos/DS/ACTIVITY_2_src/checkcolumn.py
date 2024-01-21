import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'data/class_credit_score.csv'  # Replace with the actual file path
my_data = pd.read_csv(file_path)

# Displaying all values in the 'credit_mxi' column
column_values = my_data['NumofDelayedPayment'].unique()
freqd = my_data['NumofDelayedPayment'].value_counts()

print(column_values)
print(freqd)
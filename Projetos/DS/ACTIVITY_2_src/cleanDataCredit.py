import csv
import math
import io
import pandas as pd
import re

def encode_credit_mix(input_file, output_file):
    # Read the original CSV file
    df = pd.read_csv(input_file)

    # Define mapping of categories to numerical values
    encoding_map = {
        'Bad': 0,
        'Standard': 1,
        'Good': 2
    }

    # Apply the ordinal encoding to 'CreditMix' column
    df['CreditMix'] = df['CreditMix'].map(encoding_map)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(output_file, index=False)

def update_credit_history_age(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Function to convert years and months to total months
    def convert_to_months(entry):
        if isinstance(entry, str):  # Check if entry is a string
            parts = entry.split()
            years = int(parts[0])
            months = int(parts[3])
            total_months = (years * 12) + months
            return total_months
        else:
            return entry  # Return non-string values as is

    # Update the 'Credit_History_Age' column
    df['Credit_History_Age'] = df['Credit_History_Age'].apply(convert_to_months)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)


def encode_payment_behavior_ordinal(input_file, output_file):
    # Read the original CSV file
    df = pd.read_csv(input_file)

    # Define mapping of categories to numerical values
    encoding_map = {
        'Low_spent_Small_value_payments': 1,
        'Low_spent_Medium_value_payments': 2,
        'Low_spent_Large_value_payments': 3,
        'High_spent_Small_value_payments': 4,
        'High_spent_Medium_value_payments': 5,
        'High_spent_Large_value_payments': 6
    }

    # Apply the ordinal encoding to 'Payment_Behaviour' column
    df['Payment_Behaviour'] = df['Payment_Behaviour'].map(encoding_map)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(output_file, index=False)

# Function to remove a column by index
def remove_column(input_file, output_file, column_index):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            del row[column_index]  # Remove the column by index
            writer.writerow(row)

# Function to encode month column cyclically
def encode_month(input_file, output_file):
    months = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # Create a StringIO object to read and write CSV data in memory
    output_data = io.StringIO()
    
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(output_data, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            month = row['Month']
            sin_value = math.sin((2 * math.pi * months[month]) / 12) + 1
            row['Month'] = round(sin_value,3)
            writer.writerow(row)

    # Write the modified CSV data back to the output file
    with open(output_file, 'w', newline='') as outfile:
        outfile.write(output_data.getvalue())

def encode_payment_min_amount(input_file, output_file):
    # Read the original CSV file
    df = pd.read_csv(input_file)

    # Define mapping of categories to numerical values
    encoding_map = {
        'Yes': 1,
        'No': 0,
        'NM': None  # Treat 'NM' as missing or undefined
    }

    # Apply the encoding to 'Payment_Min_Amount' column
    df['Payment_of_Min_Amount'] = df['Payment_of_Min_Amount'].map(encoding_map)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(output_file, index=False)

def encode_occupation_dummies(input_file, output_file):
    # Read the original CSV file
    df = pd.read_csv(input_file)

    # Perform dummification (one-hot encoding) on 'Occupation' column
    df_encoded = pd.get_dummies(df['Occupation'], prefix='Occupation')

    # Concatenate the encoded columns to the original DataFrame
    df = pd.concat([df, df_encoded], axis=1)

    # Drop the original 'Occupation' column
    df = df.drop('Occupation', axis=1)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(output_file, index=False)

def encode_credit_score(input_file, output_file):
    # Read the original CSV file
    df = pd.read_csv(input_file)

    # Define mapping of categories to numerical values
    encoding_map = {
        'Good': 1,
        'Poor': 0
    }

    # Apply the encoding to 'Credit_Score' column
    df['Credit_Score'] = df['Credit_Score'].map(encoding_map)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(output_file, index=False)

def consolidate_and_save(input_csv, output_csv, columns_to_consolidate):
    # Read the input CSV into a DataFrame
    df = pd.read_csv(input_csv)
    
    def consolidate_columns(df, column_name):
        df[column_name] = df[column_name] + df[f'and {column_name}']
        df[f'and {column_name}'] = 0
        df[column_name] = df[column_name].apply(lambda x: 1 if x >= 1 else 0)
    
    for column in columns_to_consolidate:
        consolidate_columns(df, column)
    
    # Drop the duplicate columns (those with 'and')
    columns_to_drop = [f'and {column}' for column in columns_to_consolidate]
    df = df.drop(columns=columns_to_drop)
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

def encode_loan_type_dummies(input_file, output_file):
    # Read the original CSV file
    df = pd.read_csv(input_file)

    # Perform dummification (one-hot encoding) on 'Type_of_Loan' column
    df_encoded = df['Type_of_Loan'].str.get_dummies(sep=', ')

    # Concatenate the encoded columns to the original DataFrame
    df = pd.concat([df, df_encoded], axis=1)

    # Drop the original 'Type_of_Loan' column
    df = df.drop('Type_of_Loan', axis=1)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(output_file, index=False)


# AGE IS CORRUPTED
def clean_age_column(input_file, output_file):
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(input_file)

    # Clean the 'age' column
    def clean_age(age):
        try:
            age = float(age)
            if 0 <= age <= 120:
                return age
            else:
                return None  # Return None for values outside the valid range
        except ValueError:
            return None  # Return None for non-numeric values

    data['Age'] = data['Age'].apply(clean_age)

    # Filter out rows with invalid age values
    cleaned_data = data.dropna(subset=['Age'])

    # Save the cleaned data to a new CSV file
    cleaned_data.to_csv(output_file, index=False)

def update_delay_column(input_file, output_file):
    # Read the CSV file
    data = pd.read_csv(input_file)

    # Update the 'Delay_from_due_date' column
    data['Delay_from_due_date'] = data['Delay_from_due_date'].apply(lambda x: x + 6)

    # Save the updated data to a new CSV file
    data.to_csv(output_file, index=False)

def replace_false_true(input_file, output_file):
    # Read the CSV file
    data = pd.read_csv(input_file)
    
    # Replace values in the entire DataFrame
    data = data.replace('False', 0, inplace=True)
    data = data.replace('True', 1, inplace=True)
    
    # Save the modified data to a new CSV file
    data.to_csv(output_file, index=False)

def remove_negative_values(input_file, output_file):
    # Read the CSV file
    data = pd.read_csv(input_file)
    
    # Loop through each column and remove negative values
    for column in data.columns:
        data[column] = data[column].apply(lambda x: x if x >= 0 else None)
    
    # Save the modified data to a new CSV file
    data.to_csv(output_file, index=False)

def transform_negative_values(input_file, output_file):
    # Read the CSV file
    data = pd.read_csv(input_file)
    
    # Loop through each column and transform negative values
    for column in data.columns:
        min_val = data[column].min()
        print(min_val)
        # Check if the minimum value is negative
        if min_val < 0:
            data[column] = data[column].apply(lambda x: x - min_val)
    
    # Save the modified data to a new CSV file
    data.to_csv(output_file, index=False)

# Replace 'input_file.csv' with the path to your CSV file
input_file_path = 'data/class_credit_score.csv'
output_file_path = 'data/clean_class_credit_score.csv'  # Output file without the specified column

tmp1 = 'tmp/tmpfile.csv'
tmp2 = 'tmp/tmpfile2.csv'

# REMOVE IDS and NAME
remove_column(input_file_path, tmp1, 0)
remove_column(tmp1, tmp2, 0)
remove_column(tmp2, tmp1, 1)

# MONTH ENCODING USING CYCLIC METHOD
encode_month(tmp1, tmp2)

# REMOVE SSN
remove_column(tmp2,tmp1,2)

# UPDATE CREDIT HISTORY 
update_credit_history_age(tmp1,tmp2)

# PAYMENT BEHAVIOUR
encode_payment_behavior_ordinal(tmp2,tmp1)

# CREDIT MIX ENCODE
encode_credit_mix(tmp1,tmp2)

# BINARY TEXT VARIABLES
encode_payment_min_amount(tmp2,tmp1)
encode_credit_score(tmp1,tmp2)

# DUMMIFICATION ON OCCUPATION
encode_occupation_dummies(tmp2,tmp1)

# DUMMIFICATION ON TYPE OF LOAN 
encode_loan_type_dummies(tmp1,tmp2)

columns_to_consolidate = [
    'Auto Loan', 'Credit-Builder Loan', 'Debt Consolidation Loan',
    'Home Equity Loan', 'Mortgage Loan', 'Not Specified',
    'Payday Loan', 'Personal Loan', 'Student Loan'
]

consolidate_and_save(tmp2,tmp1,columns_to_consolidate)

clean_age_column(tmp1,output_file_path)

print("Sucess!")
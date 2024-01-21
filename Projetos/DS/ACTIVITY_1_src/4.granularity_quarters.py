import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('data/class_credit_score.csv')

# Map months to quarters (assuming quarters start from January to March, April to June, etc.)
quarter_map = {
    'January': 'Q1',
    'February': 'Q1',
    'March': 'Q1',
    'April': 'Q2',
    'May': 'Q2',
    'June': 'Q2',
    'July': 'Q3',
    'August': 'Q3',
    'September': 'Q3',
    'October': 'Q4',
    'November': 'Q4',
    'December': 'Q4'
}

# Create a new column for quarters based on the 'month' column
data['quarter'] = data['Month'].map(quarter_map)

# Get the counts of records in each quarter
quarter_counts = Counter(data['quarter'])

# Create a sorted list of counts for all quarters in order
quarters_order = ['Q1', 'Q2', 'Q3', 'Q4']
sorted_counts = [quarter_counts[q] for q in quarters_order]

# Create a bar plot using matplotlib
plt.figure(figsize=(8, 6))  # Set the figure size
plt.bar(quarters_order, sorted_counts, color='skyblue')  # Create a bar plot
plt.title('Number of Records per Quarter')  # Set the title of the plot
plt.xlabel('Quarter')  # Set the label for x-axis
plt.ylabel('Number of Records')  # Set the label for y-axis
plt.xticks(rotation=0)  # Set x-axis labels
plt.grid(axis='y')  # Add gridlines for y-axis
plt.tight_layout()  # Adjust layout for better appearance

# Save the plot as an image file (e.g., PNG, JPG, PDF)
plt.savefig('images/SET_2_granularity_quarters.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

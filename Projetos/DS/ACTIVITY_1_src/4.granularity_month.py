import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from calendar import month_name

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('data/class_credit_score.csv')

# Get the counts of each month
month_counts = Counter(data['Month'])

# Create a dictionary with all months and their counts, including zero counts
all_months = {month: month_counts.get(month, 0) for month in month_name[1:]}

# Create a sorted list of counts for all months in order
sorted_counts = [all_months[month] for month in month_name[1:]]

# Create a bar plot using matplotlib
plt.figure(figsize=(10, 6))  # Set the figure size
plt.bar(month_name[1:], sorted_counts, color='skyblue')  # Create a bar plot
plt.title('Number of Records per Month')  # Set the title of the plot
plt.xlabel('Month')  # Set the label for x-axis
plt.ylabel('Number of Records')  # Set the label for y-axis
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(axis='y')  # Add gridlines for y-axis
plt.tight_layout()  # Adjust layout for better appearance

# Save the plot as an image file (e.g., PNG, JPG, PDF)
plt.savefig('images/SET_2_granularity_month.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

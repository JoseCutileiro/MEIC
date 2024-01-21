import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas DataFrame
data = pd.read_csv('data/class_pos_covid.csv')

# Count records by 'State'
state_counts = data['State'].value_counts()

# Sort state counts by index (state names in alphabetical order)
state_counts = state_counts.sort_index()

# Plotting
plt.figure(figsize=(10, 6))
state_counts.plot(kind='bar', color='skyblue')
plt.xlabel('States')
plt.ylabel('Number of Records')
plt.title('Number of Records per State')
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig('images/SET_1_granularity_states.png')
plt.show()
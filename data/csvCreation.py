import pandas as pd

# Load the data
file_path = 'GC_from_google.csv'
data = pd.read_csv(file_path)

print(data.shape[1]-3)

# Drop the unnecessary columns
data = data.drop(columns=['Identifier', 'Fish_Type', 'Replicates'])

# Assuming columns include 'Fish', 'Position', 'Technical replicate', and measurement columns
# Drop the 'Technical replicate' column for aggregation
columns_to_group = ['Fish_ID', 'Position']

# Calculate the median and average for each position in each fish
median_df = data.groupby(columns_to_group).median().reset_index()
average_df = data.groupby(columns_to_group).mean().reset_index()

# Save the results as new CSV files
median_output_path = 'median_data.csv'
average_output_path = 'average_data.csv'

median_df.to_csv(median_output_path, index=False)
average_df.to_csv(average_output_path, index=False)

print(f'Median data saved to: {median_output_path}')
print(f'Average data saved to: {average_output_path}')


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = 'data_GC.csv'
data = pd.read_csv(file_path)

# Select only numeric columns, excluding the categorical columns
numeric_data = data.select_dtypes(include=['number'])

# Calculate the correlation matrix
corr_matrix = numeric_data.corr()

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(25, 20))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Plot of Numeric Columns')
plt.show()
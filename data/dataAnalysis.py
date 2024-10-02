import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
file_path = 'dataEdited.csv'
data = pd.read_csv(file_path)

# Convert 'Fish_Type' and 'Position' to categorical
data['Fish_Type'] = data['Fish_Type'].astype('category')
data['Position'] = data['Position'].astype('category')
# data = data[data['Fish ID'].isin(["S01", "S02", "S03", "S04", "S05", "S06"])]
data = data[data['Fish ID'].isin(["S07", "S08", "S09", "S10", "S11", "S12"])]

# Example of using the function
# '1154.738525390625', '1160.1827392578125', '1165.6268310546875', '1699.148926', '1704.593017578125', '1710.037109', '1715.481201171875', '1720.925293', '1726.3695068359375', '1731.8135986328125'
selected_features = ['Feed', 'Fish_Type', 'Position', 'Lipid_%', 'C20:5n3']  # Replace with the actual feature names
hue_feature = 'Position'  # Replace with the feature name for color

sns.pairplot(data[selected_features], hue=hue_feature)
plt.show()

# Create separate plots for categorical vs numeric relationships
# Example with 'Fish_Type' and 'Lipid_%'
sns.catplot(x='Fish_Type', y='Lipid_%', hue='Feed', data=data, kind='box')
plt.show()

# Example with 'Position' and 'C20:5n3'
sns.catplot(x='Position', y='C20:5n3', hue='Feed', data=data, kind='violin')
plt.show()
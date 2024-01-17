import pandas as pd
import numpy as np

# Define the number of samples and features
num_samples = 10000
num_features = 10

# Create a random seed for reproducibility
np.random.seed(0)

# Generate categorical features with varying numbers of categories (between 2 and 5)
data = {}
for i in range(num_features):
    num_categories = np.random.randint(2, 6)  # Randomly choose between 2 and 5 categories
    categories = [f'Category_{i}_{j}' for j in range(num_categories)]
    data[f'Feature_{i}'] = np.random.choice(categories, size=num_samples)

# Generate labels
labels = ['alive', 'dead', 'coma']
data['Label'] = np.random.choice(labels, size=num_samples)

# Create the DataFrame
df = pd.DataFrame(data)

# Shuffle the DataFrame to ensure labels and features are randomly distributed
df = df.sample(frac=1).reset_index(drop=True)

# Save the dataset to a CSV file
df.to_csv('../data/synthetic_cardiac_data.csv', index=False)

print(df.head())  # Print the first few rows to verify

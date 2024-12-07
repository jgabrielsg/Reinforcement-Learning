import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Load the dataset
df = pd.read_csv('Sales.csv')

# Fill missing values with mean of each column (assuming normal distribution)
for col in df.columns[:-1]:
    df[col] = df[col].fillna(df[col].mean())

# Remove outlier: more than 100000 USD
outlier_filter = np.abs(df['Price'] - df['Price'].mean()) > 10000
df.dropna(subset=outlier_filter, inplace=True)

# Create state-specific dataframes with missing values and outliers
state_data = []
for state in ['Paraná', 'Acre']:
    for i, row in df.iterrows():
        if np.isnan(row['Store']):
            # Remove outlier: more than 100000 USD
            outlier_filter = (df.loc[row, 'Price'] - df.loc[row, 'Price'].mean()) > 10000
            df.dropna(subset=outlier_filter, inplace=True)
            state_data.append({
                'Date': row['Date'],
                'Store': int(row['Store']),
                'State': state,
                'Missing_Price': np.nan if outlier_filter else None,
                'Outlier_Market_Dist': 0
            })
state_df = pd.DataFrame(state_data)

# Create a new dataframe with the desired columns and remove missing values
df = df.dropna().copy()

# Convert Date to datetime and extract month
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# Group by state and Month, and count sales per month
sales_count = df.groupby(['State', 'Month']).size().reset_index(name='Count')

# Create visualizations
plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
sales_count.plot(kind='bar')
plt.title('Sales Count by State and Month')
plt.xlabel('State')
plt.ylabel('Count')
plt.xticks(rotation=45)

plt.subplot(1,2,2)
df.groupby(['Store', 'State'])['Price'].mean().plot(kind='bar')
plt.title('Average Price per Store and State')
plt.xlabel('Store & State')

# Display plots
plt.tight_layout()
plt.show()

# Save the data to a new CSV file for further analysis
sales_count.to_csv('Sales_by_state_and_month.csv', index=False)
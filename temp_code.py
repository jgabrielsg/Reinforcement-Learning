# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Sales.csv file into a DataFrame
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace missing values with mean for numerical columns and mode/median for categorical columns
def replace_missing_values(data):
    # Select numerical columns
    num_cols = ['Price']
    
    # Iterate through each column in the DataFrame
    for col in data.columns:
        if col not in num_cols:
            # Replace missing values with the mean of the column
            data[col] = data[col].fillna(data[col].mean())
            
            # Replace outliers (more than 2 standard deviations away from the mean)
            Q1 = np.percentile(data[col], 25)
            Q3 = np.percentile(data[col], 75)
            IQR = Q3 - Q1
            data[col] = np.where((data[col] < (Q1 - 2 * IQR)) | (data[col] > (Q3 + 2 * IQR)), data[col].median(), data[col])
            
    # Replace missing values with mode/median for categorical columns
    categories = ['Store', 'State']
    for category in categories:
        data[category] = data[category].fillna(data['Store'].mode().values[0])
        
    return data

# Create a new column to indicate if the sale is valid (not null and not an outlier)
def create_valid_column(data):
    # Set the mask to include only rows with no missing values or outliers
    valid_mask = ~(data.isnull() | ((np.abs(np.subtract(data['Price'], np.mean(data['Price')))) > 1000) | 
                          (data['Store'].isin(['São Paulo', 'Florianópolis']))))
    
    # Create a new column with the mask and fill null values with NaN
    data['valid'] = valid_mask.astype('bool')
    data.loc[~valid_mask, 'valid'] = np.nan
    
    return data

# Plot sales per state
def plot_sales_per_state(data):
    plt.figure(figsize=(10,6))
    sns.countplot(x='State', hue='valid', data=data)
    plt.title("Sales by State")
    plt.show()

# Plot sales per month of the year
def plot_sales_per_month(data):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    for month in months:
        month_data = data[data['Date'].dt.month == int(month)]
        plt.figure(figsize=(10,6))
        sns.countplot(x='State', hue=month_data['valid'], data=month_data)
        plt.title(f"Sales by Month of the Year: {month}")
        plt.show()

# Main function
def main():
    file_path = 'Sales.csv'
    
    # Load the Sales.csv file into a DataFrame
    data = load_data(file_path)
    
    # Replace missing values with mean for numerical columns and mode/median for categorical columns
    data = replace_missing_values(data)
    
    # Create a new column to indicate if the sale is valid (not null and not an outlier)
    data = create_valid_column(data)
    
    # Plot sales per state
    plot_sales_per_state(data)
    
    # Plot sales per month of the year
    plot_sales_per_month(data)

if __name__ == "__main__":
    main()
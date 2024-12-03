# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load data from CSV file
def load_data(file_name):
    try:
        data = pd.read_csv(file_name)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")

# Remove missing values
def remove_missing_values(data):
    # Replace null values with mean of each column
    for col in data.columns:
        mean = data[col].mean()
        data[col] = np.where(np.isnan(data[col]), mean, data[col])
    
    return data

# Find outliers (more than 2 std deviations away from the mean)
def find_outliers(data):
    # Replace null values with mean of each column
    for col in data.columns:
        mean = data[col].mean()
        data[col] = np.where(np.isnan(data[col]), mean, data[col])
    
    # Calculate standard deviation and z-score
    std_dev = data.std()
    z_scores = np.abs((data - data.mean()) / std_dev)
    
    # Find outliers (more than 2 std deviations away from the mean)
    outlier_mask = z_scores > 2
    
    # Replace outliers with mean of each column
    for col in data.columns:
        if outlier_mask[col]:
            data[col] = np.where(outlier_mask[col], data[col].mean(), data[col])
    
    return data

# Create visualizations
def create_visualizations(data):
    # Sales per state
    sales_per_state = data.groupby('State')['Price'].sum().reset_index()
    plt.bar(sales_per_state['State'], sales_per_state['Price'])
    plt.xlabel('State')
    plt.ylabel('Sales Amount (USD)')
    plt.title('Sales per State')
    plt.show()

    # Sales per month of the year
    monthly_sales = data.groupby(['Date', 'Month'])['Price'].sum().reset_index()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month in months:
        sales_per_month = monthly_sales[monthly_sales['Month'] == month]
        plt.plot(sales_per_month['Date'], sales_per_month['Price'])
        plt.title(f'Sales per Month of the Year ({month})')
        plt.xlabel('Date')
        plt.ylabel('Sales Amount (USD)')
        plt.show()

# Main function
def main():
    file_name = 'Sales.csv'
    
    # Load data from CSV file
    data = load_data(file_name)
    
    # Remove missing values
    data = remove_missing_values(data)
    
    # Find outliers (more than 2 std deviations away from the mean)
    data = find_outliers(data)
    
    # Create visualizations
    create_visualizations(data)

if __name__ == "__main__":
    main()
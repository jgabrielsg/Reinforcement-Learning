import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

# Define functions to handle input, find outliers, clean data, and main logic
def load_data(data_path):
    try:
        sales_data = pd.read_csv(data_path)
        return sales_data
    
    except FileNotFoundError:
        print(f"The file {data_path} does not exist.")
        return None
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def find_outliers(sales_data):
    """
    Find outliers in the 'Price' column.
    
    Parameters:
    sales_data (pd.DataFrame): DataFrame containing 'Date', 'Store', and 'State' columns, as well as a 'Price' column to detect outliers.

    Returns:
    pd.DataFrame: A new DataFrame with outliers removed from the original data.
    """
    # Find dates where there are missing values
    missing_values_indices = sales_data[sales_data.isnull().any(axis=1)].index
    
    # Remove duplicates based on date and price
    for index in list(missing_values_indices):
        if not (sales_data.loc[index, 'Date'] == sales_data.loc[missing_values_indices[index], 'Date']).all() or \
            (not (sales_data.loc[index, 'Price'] == sales_data.loc[missing_values_indices[index], 'Price']).all()):
            sales_data.drop(index, inplace=True)
    
    # Find dates where there are missing values in the date column
    date_missing_values = sales_data[sales_data['Date'].isnull()].index
    
    # Remove duplicates based on date and price
    for index in list(date_missing_values):
        if not (sales_data.loc[index, 'Date'] == sales_data.loc[date_missing_values[index], 'Date']).all() or \
            (not (sales_data.loc[index, 'Price'] == sales_data.loc[date_missing_values[index], 'Price']).all()):
            sales_data.drop(index, inplace=True)
    
    # Find dates where there are missing values in the price column
    price_missing_values = sales_data[sales_data['Price'].isnull()].index
    
    # Remove duplicates based on date and price
    for index in list(price_missing_values):
        if not (sales_data.loc[index, 'Date'] == sales_data.loc[price_missing_values[index], 'Date']).all() or \
            (not (sales_data.loc[index, 'Price'] == sales_data.loc[price_missing_values[index], 'Price']).all()):
            sales_data.drop(index, inplace=True)
    
    return sales_data

def clean_and_preprocess(sales_data):
    """
    Clean and preprocess data by removing duplicates based on date, price, store, and state columns.
    
    Parameters:
    sales_data (pd.DataFrame): DataFrame containing necessary columns to remove duplicates.
    
    Returns:
    pd.DataFrame: A new DataFrame with duplicates removed from the original data.
    """
    # Remove duplicates based on date
    for index in list(sales_data.index):
        if not sales_data.loc[index, 'Date'].isnull():
            del sales_data.loc[index]
    
    # Remove duplicates based on price
    for index in list(sales_data.index):
        if not sales_data.loc[index, 'Price'].isnull():
            del sales_data.loc[index]
    
    # Remove duplicates based on store and state columns
    for index in list(sales_data.index):
        if not sales_data.loc[index, 'Store'].isnull() and not sales_data.loc[index, 'State'].isnull():
            del sales_data.loc[index]
    
    return sales_data

def main():
    data_path = 'Sales.csv'  # Update this to your data path
    
    # Load the data
    sales_data = load_data(data_path)
    
    if sales_data is None:
        print("No data found.")
        return
    
    # Find outliers in the price column
    outlier_data = find_outliers(sales_data)
    
    # Clean and preprocess the data
    cleaned_sales_data = clean_and_preprocess(outlier_data)
    
    # Print data statistics
    print(f"Number of rows: {len(cleaned_sales_data)}")
    print(f"Number of columns: {len(cleaned_sales_data.columns)}")
    print(f"Data type distribution:\n{cleaned_sales_data.dtypes}")
    
    # Plot sales per state and month of the year
    sales_per_state = cleaned_sales_data.groupby('State')['Price'].sum().to_dict()
    for state, value in sales_per_state.items():
        print(f"{state}: {value:.2f}")
    monthly_sales = {}
    for date in set(cleaned_sales_data['Date']):
        month = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m')
        sales_per_month = cleaned_sales_data[cleaned_sales_data['Date'] == date]['Price'].sum()
        if month not in monthly_sales:
            monthly_sales[month] = sales_per_month
        else:
            monthly_sales[month] += sales_per_month
    
    for month, value in monthly_sales.items():
        print(f"{month}: {value:.2f}")

if __name__ == "__main__":
    main()
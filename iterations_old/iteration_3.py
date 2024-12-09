import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def load_data(file_name):
    """
    Load the sales data from a CSV file.
    
    Parameters:
    file_name (str): The name of the CSV file.
    
    Returns:
    pd.DataFrame: The loaded sales data.
    """
    try:
        # Check if the file exists
        if not pd.isnull(file_name).any():
            raise FileNotFoundError("The specified file does not exist.")
        
        # Load the dataset from a csv file
        data = pd.read_csv(file_name)
        
        return data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def remove_outliers_and_missing_values(data):
    """
    Remove outliers and missing values from the data.
    
    Parameters:
    data (pd.DataFrame): The loaded sales data.
    
    Returns:
    pd.DataFrame: The cleaned sales data.
    """
    try:
        # Outlier detection using z-score
        Z_score = 3
        
        # Replace null values with mean of that column, except for Price which doesn't require it
        for col in data.columns:
            if 'Price' not in col:
                data[col].fillna(data[col].mean(), inplace=True)
        
        return data
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

def clean_data(data):
    """
    Clean the data by removing outliers and null values.
    
    Parameters:
    data (pd.DataFrame): The cleaned sales data.
    
    Returns:
    pd.DataFrame: The fully cleaned sales data.
    """
    try:
        # Outlier detection using z-score
        Z_score = 3
        
        # Replace null values with mean of that column, except for Price which doesn't require it
        for col in data.columns:
            if 'Price' not in col and 'Quantity' not in col:
                data[col].fillna(data[col].mean(), inplace=True)
        
        # Fill missing values in other columns using median
        data = data.fillna(data.median())
        
        return data
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

def visualize_sales(data):
    """
    Visualize sales per state and month.
    
    Parameters:
    data (pd.DataFrame): The cleaned sales data.
    """
    # Sales per state by month
    monthly_sales = data.groupby(['Date', 'State']).agg({'Price': 'mean'}).reset_index()
    
    # Pivot to get the count of each sale per state
    monthly_sales = monthly_sales.pivot_table(values='Price', index=['Date', 'State'], aggfunc='count')
    
    # Plot sales per state per month
    plt.figure(figsize=(10, 6))
    monthly_sales.plot(kind='bar')
    plt.title('Sales per State and Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Sales')
    plt.legend(title='Store', bbox_to_anchor=(1.05, 1))  # Add a legend
    plt.tight_layout()  # Adjust layout to fit the legend
    plt.show()

def main():
    file_name = 'Sales.csv'
    
    try:
        data = load_data(file_name)
        
        # Remove outliers and missing values
        cleaned_data = remove_outliers_and_missing_values(data)
        
        # Fill missing values in other columns using median
        cleaned_data = clean_data(cleaned_data)
        
        # Visualize sales per state and month
        visualize_sales(cleaned_data)
        
    except Exception as e:
        print(f"Error running the script: {str(e)}")

if __name__ == "__main__":
    main()
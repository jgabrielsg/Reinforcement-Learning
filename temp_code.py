# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def read_file(file_name):
    """
    Reads a csv file and checks for missing values and outliers.

    Parameters:
    file_name (str): Name of the csv file

    Returns:
    df (pd.DataFrame): DataFrame with sales data
    missing_values (int): Number of missing values in the DataFrame
    outliers (pd.Series): Outliers in the DataFrame
    """
    
    # Read the csv file
    try:
        if not file_name.endswith('.csv'):
            print("Please provide a valid csv file name.")
            return None, 0, pd.DataFrame(columns=['Date', 'State'])
        
        # Read the csv file
        file_path = f"sales_{datetime.now().strftime('%Y%m%d')}.csv"
        df = pd.read_csv(file_path)
        
        # Check for missing values and outliers
        missing_values = df.isnull().sum()
        outliers = df[(df['Price'] > 100000) | (df['Price'] < -100000)]
        
        return df, missing_values, outliers
    
    except Exception as e:
        print(f"Error occurred while reading the file: {e}")
        return None, 0, pd.DataFrame(columns=['Date', 'State'])

def clean_data(file_name):
    """
    Cleans the sales.csv by dropping rows with missing values and outliers,
    grouping by State and summing Price. Also plots Sales per state and
    per month of the year.

    Parameters:
    file_name (str): Name of the csv file

    Returns:
    df (pd.DataFrame): Cleaned DataFrame
    """
    
    # Define a function to drop rows with missing values and outliers
    def drop_na_outliers(df):
        """
        Drops rows with missing values and outliers.
        
        Parameters:
        df (pd.DataFrame): DataFrame with sales data
        
        Returns:
        df (pd.DataFrame): Cleaned DataFrame
        """
        
        # Check for missing values and outliers
        cleaned_df = df.dropna(subset=missing_values.index)
        cleaned_outliers = cleaned_df[~cleaned_df['Price'].isin(outliers.index)]
        
        return cleaned_df, cleaned_outliers
    
    # Define a function to plot Sales per state and per month of the year
    def plot_sales(file_name):
        """
        Plots Sales per state and per month of the year.

        Parameters:
        file_name (str): Name of the csv file

        Returns:
        None
        """
        
        # Read the csv file
        df, missing_values, outliers = read_file(file_name)
        
        if df is not None:
            # Group by State and sum Price
            sales_by_state = df.groupby('State')['Price'].sum().reset_index()
            
            # Plot Sales per state
            plt.figure(figsize=(10,6))
            sns.barplot(x='State', y='Price', data=sales_by_state)
            plt.title("Sales per State")
            plt.xlabel("State")
            plt.ylabel("Total Price")
            plt.show()
            
            # Group by Month and sum Price
            sales_by_month = df.groupby('Date')['Price'].sum().reset_index()
            
            # Plot Sales per month of the year
            plt.figure(figsize=(10,6))
            sns.barplot(x='Month', y='Price', data=sales_by_month)
            plt.title("Sales per Month of the Year")
            plt.xlabel("Month")
            plt.ylabel("Total Price")
            plt.show()
    
    # Define a function to check for duplicate rows by date and State
    def check_duplicates(file_name):
        """
        Checks for duplicate rows by date and State.

        Parameters:
        file_name (str): Name of the csv file

        Returns:
        None
        """
        
        # Read the csv file
        df, missing_values, outliers = read_file(file_name)
        
        if df is not None:
            # Check for duplicate rows by date and State
            duplicate_rows = cleaned_df.duplicated(subset=['Date', 'State'])
            print("Duplicate rows found.")
    
    # Main function
    def main():
        file_name = 'sales.csv'
        
        # Read the csv file
        df, missing_values, outliers = read_file(file_name)
        
        if df is not None:
            cleaned_df, cleaned_outliers = drop_na_outliers(df)
            
            plot_sales(file_name)  # Plot Sales per state and per month of the year
            
            check_duplicates(file_name)  # Check for duplicate rows by date and State
    
    return clean_data

# Execute the function
def main():
    file_name = 'sales.csv'
    result = read_file(file_name)
    
    if result is not None:
        main()

if __name__ == "__main__":
    main()
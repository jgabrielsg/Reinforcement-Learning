import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import seaborn as sns

# Function to load data
def load_data(file_path):
    try:
        # Load the Sales.csv file
        sales_df = pd.read_csv(file_path)
        
        # Check if the file is not empty
        if sales_df.empty:
            print("No data in the file. Please check the file contents.")
            return None
        
        return sales_df
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
    except pd.errors.EmptyDataError:
        print(f"No data in the file. Please check the file contents.")
        return None

# Function to clean and preprocess data
def clean_data(sales_df):
    try:
        # Check for missing values
        if sales_df.isnull().values.any():
            print("Missing values detected.")

            # Identify rows with missing values
            missing_values = sales_df[sales_df.isnull().any(axis=1)]

            # Replace missing values with a specific value or drop the row
            sales_df.loc[missing_values.index, 'Price'] = np.nan

        # Remove outliers (more than 2 standard deviations from the mean)
        q1 = sales_df['Price'].quantile(0.25)
        q3 = sales_df['Price'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Replace outliers with a specific value or drop the row
        sales_df.loc[sales_df['Price'] > (upper_bound + 2 * iqr), 'Price'] = np.nan
        sales_df.loc[sales_df['Price'] < (lower_bound - 2 * iqr), 'Price'] = np.nan

        # Scale data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(sales_df[['Date', 'Price', 'Store', 'State']])

        return scaled_data
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Function to create visualizations
def create_visualizations(data):
    try:
        # Validate the 'State' value before creating a bar plot
        valid_states = ['US', 'Canada']
        
        for state in list(data['State'].unique()):
            if state not in valid_states:
                print(f"Error: '{state}' is an invalid state.")
                break
        
        # Create a figure with two subplots
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))

        # Sales per state and month of the year plots
        sales_per_state = data.groupby('State')['Price'].mean()
        sns.barplot(x=sales_per_state.index, y=sales_per_state.values, ax=axs[0])
        axs[0].set_title('Sales per State')
        axs[0].set_xlabel('State')
        axs[0].set_ylabel('Average Price')

        monthly_sales = data.groupby(pd.Grouper(key='Date', freq='M'))['Price'].sum()
        sns.lineplot(x=monthly_sales.index.strftime('%Y-%m'), y=monthly_sales.values, ax=axs[1])
        axs[1].set_title('Sales per Month of the Year')
        axs[1].set_xlabel('Month')
        axs[1].set_ylabel('Total Sales')

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Main function
def main():
    # Load data
    file_path = 'Sales.csv'
    
    if not load_data(file_path):
        return
    
    # Clean and preprocess data
    cleaned_data = clean_data(load_data(file_path))

    # Create visualizations
    create_visualizations(cleaned_data)

if __name__ == "__main__":
    main()
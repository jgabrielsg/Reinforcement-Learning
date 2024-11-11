import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads and returns a DataFrame from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data, or raises an exception if the file is not found or cannot be loaded.
    """

    try:
        return pd.read_csv(file_path)
    
    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found.")
        raise e
    
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file {file_path} is empty.")
        raise e


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and preprocesses the data by removing missing values, outliers, normalizing or scaling, and handling categorical variables.

    Args:
        data (pd.DataFrame): The cleaned data.

    Returns:
        pd.DataFrame: The preprocessed data.
    """

    try:
        # Remove rows with missing values
        data = data.dropna()
        
        # Find and remove outliers (more than 2 standard deviations away from the mean)
        scaler = StandardScaler()
        data['Sales'] = scaler.fit_transform(data[['Sales']])
        outliers = np.abs((data['Sales'] - np.mean(data['Sales'])) / np.std(data['Sales'])).max(axis=1) > 3
        data[outliers] = np.nan
        
        # Normalize the numerical columns
        categorical_cols = ['Category', 'Region']
        for col in categorical_cols:
            if col not in data.columns:
                continue
            
            data[col] = pd.DataFrame(data[col].astype('category').cat.codes, columns=[col])
        
        # Scale the numerical columns
        numerical_cols = ['Product', 'Subtotal']
        for col in numerical_cols:
            scaler = MinMaxScaler()
            data[col] = scaler.fit_transform(data[[col]])
        
        return data
    
    except Exception as e:
        print(f"Error processing data: {str(e)}")


def plot_sales_data(sales_data: pd.DataFrame, region: str) -> None:
    """
    Plots the sales data for a specific region.

    Args:
        sales_data (pd.DataFrame): The sales data.
        region (str): The region to plot.
    """

    try:
        # Group by region and calculate total sales
        sales_grouped = sales_data.groupby('Region')['Sales'].sum()
        
        # Plot the result
        plt.figure(figsize=(10, 6))
        sales_grouped.plot(kind="bar")
        plt.title(f"Total Sales in {region}")
        plt.xlabel("Region")
        plt.ylabel("Total Sales")
        
        # Show the plot
        plt.show()
    
    except Exception as e:
        print(f"Error plotting data: {str(e)}")


def main() -> None:
    """
    The main function.
    """

    file_paths = ["Sales1.csv", "Sales2.csv"]  # Specify multiple file paths here
    
    for file_path in file_paths:
        try:
            data = load_data(file_path)
            
            if data is not None:
                sales_data = clean_data(data)
                
                plot_sales_data(sales_data, 'State')
        
        except Exception as e:
            print(f"Error processing data: {str(e)}")


if __name__ == "__main__":
    main()
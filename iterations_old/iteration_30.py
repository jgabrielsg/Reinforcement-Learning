import pandas as pd
from datetime import datetime
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_name):
    """
    Loads data from a CSV file.
    
    Args:
        file_name (str): Name of the CSV file.
    
    Returns:
        pandas.DataFrame: Loaded DataFrame.
    """
    try:
        # Load the data from a CSV file
        df = pd.read_csv(file_name)
        
        return df
    
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return None


def validate_data(df):
    """
    Validates the input data.
    
    Args:
        df (pandas.DataFrame): Input DataFrame.
    
    Returns:
        bool: True if data is valid, False otherwise.
    """
    try:
        # Check for missing values
        assert not df.isnull().values.any(), "Missing values found"
        
        # Check if all columns are numeric
        numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        assert len(numeric_columns) == len(df), f"Non-numeric columns: {', '.join(numeric_columns)}"
        
        return True
    
    except AssertionError as e:
        print(f"Error validating data: {e}")
        return False


def calculate_state_sales(df):
    """
    Calculates state R-squared values.
    
    Args:
        df (pandas.DataFrame): Input DataFrame.
    
    Returns:
        dict: Dictionary with states as keys and R-squared values as values.
    """
    try:
        # Convert Date to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Group by Region and calculate total sales for each month
        monthly_sales = df.groupby(['Region', 'Date'])['Price'].sum().reset_index()
        
        states = list(set(monthly_sales['Region']))
        r2_values = {}
        
        for state in states:
            region_data = monthly_sales[monthly_sales['Region'] == state]
            
            if not (region_data.shape[0] > 10):  
                print(f"Skipping {state} due to low sample size")
                continue
            
            X = region_data[['Date', 'Price']]
            y = region_data['Price']
            
            # Check for missing values
            assert not X.isnull().values.any(), "Missing values found in X"
            
            # Fit the model and calculate R-squared value
            try:
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict prices for a new month
                predicted_prices = model.predict(np.array([[df['Date'].max()]])[0])
                
                r2_value = np.mean((predicted_prices - y) ** 2) / (y ** 2)
                
                if not isinstance(r2_value, float):
                    raise ValueError("R-squared value is not a number")
                
                r2_values[state] = r2_value
            except Exception as e:
                print(f"Error calculating R-squared value for {state}: {e}")
        
        return dict(r2_values)
    
    except AssertionError as e:
        print(f"Error validating data: {e}")
        return None


def get_all_test_sets(df):
    """
    Gets all test sets for training and validation.
    
    Args:
        df (pandas.DataFrame): Input DataFrame.
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Training set and validation set.
    """
    try:
        # Define the features (X) and target variable (y)
        X = ['Date', 'Price']
        
        # Split data into training and testing sets
        train_x, test_x, train_y, val_test_x, val_train_y = train_test_split(X, [1]*len(X), random_state=42, test_size=0.2)
        
        val_x, val_test_x, val_train_y, val_test_y = train_test_split(X, [1]*len(X), random_state=42, test_size=0.5)
        
        return X, pd.DataFrame({'Date': range(len(test_x)), 'Price': test_x.values}), X, pd.DataFrame({'Date': range(len(val_test_x)), 'Price': val_test_x.values}), X, pd.DataFrame({'Date': range(len(val_train_y)), 'Price': val_train_y.values}), X, pd.DataFrame({'Date': range(len(val_test_y)), 'Price': val_test_y.values})
    
    except AssertionError as e:
        print(f"Error getting all test sets: {e}")
        return None


def main():
    # Load data
    file_name = "sales_data.csv"
    df = load_data(file_name)
    
    if not validate_data(df):
        print("Failed to load and validate data.")
        return
    
    # Calculate state R-squared values
    r2_values = calculate_state_sales(df)
    
    # Get all test sets
    X, train_y, val_test_x, val_train_y = get_all_test_sets(df)
    
    # Print results
    print("State R-squared values:")
    for state, r2_value in r2_values.items():
        print(f"  {state}: {r2_value}")
        
    # Plot the data and R-squared values
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='Date', y='Price', hue='Region', data=df)
    sns.barplot(x='Region', y='Price', data=train_y)
    sns.barplot(x='Region', y='Price', data=val_test_x)
    sns.barplot(x='Region', y='Price', data=val_train_y)
    
    plt.title("Data and R-squared values")
    plt.show()
    
    print("Training set and validation set:")
    for i, (x, y) in enumerate(zip(train_x, train_y)):
        print(f"X: {x}, Y: {y}")
    for i, (x, y) in enumerate(zip(val_test_x, val_train_y)):
        print(f"X: {x}, Y: {y}")


if __name__ == "__main__":
    main()
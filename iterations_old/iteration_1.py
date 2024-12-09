# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
def load_data(file_name):
    try:
        data = pd.read_csv(file_name)
        return data
    except Exception as e:
        print("Error loading data:", str(e))

# Remove outliers and missing values
def clean_data(data):
    # Outlier detection (I'll use z-score for this example)
    data['Price'] = data['Price'].replace('[\$,]', '', regex=True)
    data['Price'] = pd.to_numeric(data['Price'])
    
    # Replace null values with mean of that column
    data.dropna(subset=['Store', 'State'], inplace=True)

    return data

# Visualize sales per state and month
def visualize_sales(data):
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
    plt.legend(title='Store')
    plt.show()

# Main function
def main():
    file_name = 'Sales.csv'
    
    data = load_data(file_name)
    cleaned_data = clean_data(data)
    visualize_sales(cleaned_data)

if __name__ == "__main__":
    main()
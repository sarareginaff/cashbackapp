from pandas import DataFrame
import datetime

def define_cashback_percentage(value):
    if value < 1000:
        percentage = 0.10
    elif value < 1500:
        percentage = 0.15
    else:
        percentage = 0.2
    
    return percentage
    
def get_month(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').month
    
def get_value_by_percentage(value, percentage):
    return value * percentage

def calculate_cashback(purchases):
    # Convert to do dataframe
    df = DataFrame(purchases, columns=['Code', 'Value', 'Dth_purchase', 'Cpf', 'Status'])

    # Group data by cpf and month
    df['Month'] = df['Dth_purchase'].map(get_month)
    grouped_df = df.groupby(['Cpf', 'Month']).sum()
    
    # Calculate cashback for each group
    grouped_df['Cashback_%'] = grouped_df['Value'].map(define_cashback_percentage)
    
    # Merge data with each purchase
    df = df.merge(grouped_df.drop(columns=['Value']), 
                    left_on=['Month','Cpf'], 
                    right_on=['Month','Cpf']).drop(columns=['Month'])
    
    df['Cashback_#'] = df['Cashback_%'] * df['Value']
    
    return df
    

import datetime
from flask import current_app as app
from pandas import DataFrame


def define_purchase_status(cpf):
    status = "Validation"
    
    if(cpf in list(app.config['APPROVED_CPFS'])):
        status = "Approved"
    
    return status


def validate_purchase_register(code, value, dth_purchase, cpf):
    error = ''
    if not code:
        error += 'Codigo da compra eh necessario. '
    if not value:
        error += 'Valor da compra eh necessario. '
    if not dth_purchase:
        error += 'Data da compra eh necessaria. '
    if not cpf:
        error += 'CPF do revendedor ou da revendedora eh necessaria. '
        
    return error
   
 
def define_cashback_percentage(value):
    if value < 1000:
        percentage = 0.10
    elif value < 1500:
        percentage = 0.15
    else:
        percentage = 0.20
    
    return percentage
    

def get_month(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').month
    

def get_value_by_percentage(value, percentage):
    return value * percentage


def calculate_cashback(purchases):
    # Convert to do dataframe
    df = DataFrame(purchases, 
                    columns=['Code', 'Value', 'Dth_purchase', 'Cpf', 'Status'])

    # Group data by cpf and month
    df['Month'] = df['Dth_purchase'].map(get_month)
    grouped_df = df.groupby(['Cpf', 'Month']).sum()
    
    # Calculate cashback for each group
    grouped_df['Cashback_%'] = grouped_df['Value'].map(define_cashback_percentage)
    
    # Merge data with each purchase
    df = df.merge(grouped_df.drop(columns = ['Value']), 
                    left_on = ['Month','Cpf'], 
                    right_on = ['Month','Cpf'],
                    how = 'inner').drop(columns=['Month'])
    
    df['Cashback_#'] = df['Cashback_%'] * df['Value']
    
    return df
    

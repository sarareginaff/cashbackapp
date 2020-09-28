import datetime
from flask import current_app as app
from pandas import DataFrame


def define_purchase_status(cpf):
    """
        Define status of purchase based on cpf.

        :Parameters: 
            - cpf (string): CPF of user responsible for purchase.

        :Returns: 
            - status (string): Status of purchase

        :author: sarareginaff       
        :creation: Sep/2020
    """
    status = "Validation"
    
    if(cpf in app.config['APPROVED_CPFS'].split(',')):
        status = "Approved"
    
    return status


def validate_purchase_register(code, value, dth_purchase, cpf):
    """
        Validate if purchase register data is correct.

        :Parameters: 
            - code (string): purchase code
            - value (number): purchase value
            - dth_purchase (string): date of purchase in format %Y-%m-%d %H:%M:%S
            - cpf (string): CPF of user responsible for purchase.

        :Returns: 
            - error (string): Error of data. Can be empty

        :author: sarareginaff       
        :creation: Sep/2020
    """
    error = ''
    if not code:
        error += 'Codigo da compra eh necessario. '
    if not value:
        error += 'Valor da compra eh necessario. '
    if not dth_purchase:
        error += 'Data da compra eh necessaria. '
    else:
        try:
            get_month(dth_purchase)
        except:
            error += 'Data nao esta no formato %Y-%m-%d %H:%M:%S.'
    if not cpf:
        error += 'CPF do revendedor ou da revendedora eh necessaria. '
        
    return error
   
 
def define_cashback_percentage(value):
    """
        Define cashback percentage based on value.

        :Parameters: 
            - value (number): purchases value

        :Returns: 
            - percentage (number): cashback percentage

        :author: sarareginaff       
        :creation: Sep/2020
    """
    if value < 1000:
        percentage = 0.10
    elif value < 1500:
        percentage = 0.15
    else:
        percentage = 0.20
    
    return percentage
    

def get_month(date):
    """
        Get month of date.

        :Parameters: 
            - date (string): in format %Y-%m-%d %H:%M:%S

        :Returns: 
            - month (number): month of date

        :author: sarareginaff       
        :creation: Sep/2020
    """
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').month
    

def calculate_cashback(purchases):
    """
        Calculate cashback of list of purchases.

        :Parameters: 
            - purchases (list): list of purchases with its code, value, dth_purchase, cpf and status

        :Returns: 
            - df (dataframe): dataframe of purchases with its original information and cashback information

        :author: sarareginaff       
        :creation: Sep/2020
    """
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
    

from pandas import DataFrame

def calculate_cashback(purchases):
    # Convert to do dataframe
    df = DataFrame(purchases, columns=['code', 'value', 'dth_purchase', 'cpf'])
    
    df['Price'] = [1500 if x =='Music' else 800 for x in df['Event']] 
    df['Address'] = address
    print(df.groupby(['cpf', ]).sum())
    purchase_cashback = []
    print(type(purchases))
    # Group data by cpf
    # Group data by month
    # Calculate cashback for each group
    # Return data for each purchase

    return purchase_cashback
    

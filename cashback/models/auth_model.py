import re
import datetime
import jwt

from flask import current_app as app


def check_cpf(cpf):
    """
        Check if CPF is valid.

        :Parameters: 
            - cpf (string): cpf of user

        :Returns: 
            - verification (bool): information if cpf is valid or not

        :author: sarareginaff       
        :creation: Sep/2020
    """
    #CPF always has 11 digits
    if len(cpf) != 11:
        return False
    else:
        return True
  
      
def clean_cpf(cpf):
    """
        Remove all not-numbers digits of cpf

        :Parameters: 
            - cpf (string): cpf of user. Can have dots and hifens

        :Returns: 
            - cpf (string): cpf containing only numbers

        :author: sarareginaff       
        :creation: Sep/2020
    """
    return re.sub('[^0-9]', '', cpf)


def validate_user_register(full_name, cpf, email, password):
    """
        Validate if user register data is correct.

        :Parameters: 
            - full_name (string): Full name of new user
            - cpf (string): CPF of new user.
            - email (string): email of new user. It must have a @
            - password (string): password of new user

        :Returns: 
            - error (string): Error of data. Can be empty

        :author: sarareginaff       
        :creation: Sep/2020
    """
    error = ''
    
    if not full_name:
        error += 'Nome completo eh necessario. '
    if not cpf or not check_cpf(cpf):
        error += 'Um CPF valido eh necessario. '
    if not email or '@' not in email:
        error += 'Um e-mail valido eh necessario. '
    if not password:
        error += 'A senha eh necessaria. '
    
    return error
    
def encode_token(cpf):
    """
        Create token for user based on its cpf.

        :Parameters: 
            - cpf (string): CPF of new user.

        :Returns: 
            - token (string): created token for user
            - expire_date (datetime): token expire date

        :author: sarareginaff       
        :creation: Sep/2020
    """
    expire_date = datetime.datetime.now() + datetime.timedelta(hours=12)

    token = jwt.encode({'cpf': cpf, 'exp': expire_date}, 
                            app.config['SECRET_KEY'])
                            
    return token, expire_date

def decode_token(token):
    """
        Decode token to get its raw data.

        :Parameters: 
            - token (string): created token for user

        :Returns: 
            - data (dict): raw data used to create token

        :author: sarareginaff       
        :creation: Sep/2020
    """
    return jwt.decode(token, key=app.config['SECRET_KEY'])

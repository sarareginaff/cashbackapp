import re
import datetime
import jwt

from flask import current_app as app


def check_cpf(cpf):
    #CPF always has 11 digits
    if len(cpf) != 11:
        return False
    else:
        return True
  
      
def clean_cpf(cpf):
    return re.sub('[^0-9]', '', cpf)


def validate_user_register(full_name, cpf, email, password):
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
    expire_date = datetime.datetime.now() + datetime.timedelta(hours=12)

    token = jwt.encode({'cpf': cpf, 'exp': expire_date}, 
                            app.config['SECRET_KEY'])
                            
    return token, expire_date

def decode_token(token):
    return jwt.decode(token, key=app.config['SECRET_KEY'])

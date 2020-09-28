import datetime
from flask import request, jsonify
from functools import wraps

from cashback.db import auth_db
from cashback.models import auth_model
    
def token_required(f):
    """
        Create decorator to request token.

        :Headers: 
            - Content-Type: application/json
            - Authorization (string): token of user.
            
        :Returns:
            - current_user: Current user data

        :author: sarareginaff       
        :creation: Sep/2020
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Esta faltando o token'}), 401
        else:
            not_allowed_tokens = auth_db.get_not_allowed_tokens()
            if not_allowed_tokens and token in not_allowed_tokens:
                return jsonify({'message': '''Token nao esta habilitado. 
                                            Usuario foi deslogado'''}), 401
        try:
            data = auth_model.decode_token(token)
            
            if data['exp'] < datetime.datetime.now().timestamp():
                return jsonify({'message': 'Token expirado'}), 401
            else:
                current_user = auth_db.get_user_by_cpf(cpf=data['cpf'])
        except:
            return jsonify({'message': 'Token invalido'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
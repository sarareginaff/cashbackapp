from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from cashback.db import auth_db
from cashback.controllers import helper 
from cashback.models import auth_model


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    """
        Register new user.

        :Parameters: 
            - full_name (string): Full name of new user
            - cpf (string): CPF of new user. Can have dots and hifens
            - email (string): email of new user. It must have a @
            - password (string): password of new user
    
        :Headers: 
            - Content-Type: application/json
        
        :Returns:
            - message (string): Success if user is registered. Errors explanation if not

        :author: sarareginaff       
        :creation: Sep/2020
    """
    try:
        full_name = request.json['full_name']
        cpf = auth_model.clean_cpf(request.json['cpf'])
        email = request.json['email']
        password = request.json['password']
    
        error = auth_model.validate_user_register(full_name, cpf, email, password)

        if error != '':
            return jsonify({'message': error}), 406
        elif auth_db.get_user_by_cpf(cpf) is not None:
            return jsonify({'message': 'Ja existe um usuario cadastrado com o CPF {}'
                            .format(cpf)}), 409
    
        auth_db.insert_new_user(full_name, cpf, email, password)
        
        return jsonify({'message': 'Usuario cadastrado com sucesso'}), 200
    except Exception as err:
        return jsonify({'message': 'Nao foi possivel registrar o usuario - {}'
                        .format(err)}), 500
    

@bp.route('/login', methods=['POST'])
def login():
    """
        Login user.

        :Parameters: 
            - cpf (string): CPF of user. Can have dots and hifens
            - password (string): password of user
        
        :Headers: 
            - Content-Type: application/json

        :Returns: 
            - message (string): Success if user is registered. Errors explanation if not
            - token (string): Token of user and its expire date
            - exp (string): Token expire date

        :author: sarareginaff       
        :creation: Sep/2020
    """
    try:
        cpf = auth_model.clean_cpf(request.json['cpf'])
        password = request.json['password']
        user = auth_db.get_user_by_cpf(cpf)
        
        if user is None or not check_password_hash(user['password'], password):
            return jsonify({'message': 'CPF não encontrado ou senha incorreta.'}), 401
    
        token, expire_date = auth_model.encode_token(cpf)
        
        return jsonify({'message': 'Usuario autenticado com sucesso!', 
                        'token': token.decode('UTF-8'), 'exp': expire_date}), 200
    except Exception as err:
        return jsonify({'message': 'Erro inesperado ao autenticar usuario - {}'
                        .format(err)}), 500


@bp.route('/logout', methods=['GET'])
@helper.token_required
def logout(current_user):
    """
        Logout user.

        :Headers: 
            - Authorization (string): token of user.
            - Content-Type: application/json
        
        :Returns: 
            - message (string): Success if user is registered. Errors explanation if not

        :author: sarareginaff       
        :creation: Sep/2020
    """
    try:
        token = request.headers.get('Authorization')
        
        not_allowed_tokens = auth_db.get_not_allowed_tokens()
        not_allowed_tokens.append(token)
        
        auth_db.update_not_allowed_tokens(not_allowed_tokens)
        
        return jsonify({'message': 'Usuario fez o logout com sucesso!'}), 200
    except Exception as err:
        return jsonify({'message': 'Erro inesperado ao fazer logout - {}'
                        .format(err)}), 500



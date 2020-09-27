import functools
import datetime
import jwt
import sys
import redis
import json
from flask import (
    Blueprint, g, request, session, jsonify, current_app as app
)
from werkzeug.security import check_password_hash, generate_password_hash
from cashback.db.db import get_db
from cashback.models import auth_model

from cashback.views import helper 

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    try:
        full_name = request.json['full_name']
        cpf = request.json['cpf']
        email = request.json['email']
        password = request.json['password']
    
        db = get_db()
        error = None
    
        if not full_name:
            error = 'Nome completo eh necessario. '
        if not cpf:
            error += 'CPF eh necessario. '
        if not email:
            error += 'E-mail eh necessario. '
        if not password:
            error += 'A senha eh necessaria. '

        if error is not None:
            return jsonify({'message': error}), 406
        elif db.execute(
                'SELECT id FROM users WHERE cpf = ?', (cpf,)
            ).fetchone() is not None:
            return jsonify({'message': 'Ja existe um usuario cadastrado com o CPF {}'.format(cpf)}), 406
    

        db.execute(
            'INSERT INTO users (full_name, cpf, email, password) VALUES (?, ?, ?, ?)',
            (full_name, cpf, email, generate_password_hash(password),)
        )
        db.commit()
        
        return jsonify({'message': 'Usuario cadastrado com sucesso'}), 200
    except:
        return jsonify({'message': 'Nao foi possivel registrar o usuario - {}'.format(sys.exc_info()[0])}), 500
    
@bp.route('/login', methods=['POST'])
def login():
    try:
        cpf = request.json['cpf']
        password = request.json['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE cpf = ?', (cpf,)
        ).fetchone()

        if user is None:
            return jsonify({'Nao foi possivel encontrar usuario com este CPF.'}), 401
        elif not check_password_hash(user['password'], password):
            error = ''
            return jsonify({'message': 'Senha incorreta.'}), 401
    
        expire_date = datetime.datetime.now() + datetime.timedelta(hours=12)

        token = jwt.encode({'cpf': user['cpf'], 'exp': expire_date}, 
                            app.config['SECRET_KEY'])
        
        return jsonify({'message': 'Usuario autenticado com sucesso!', 
                        'token': token.decode('UTF-8'), 'exp': expire_date}), 200
    except:
        return jsonify({'message': 'Erro inesperado {}'.format(sys.exc_info()[0])}), 500

@bp.route('/logout', methods=['GET'])
@helper.token_required
def logout(current_user):
    token = request.headers.get('Authorization')
    r = redis.StrictRedis(host=app.config['REDIS_HOST'], 
                        port=app.config['REDIS_PORT'],
                        decode_responses=True)
    not_allowed_tokens = list(r.get('not_allowed_tokens'))
    not_allowed_tokens.append(token)
    r.set('not_allowed_tokens', json.dumps(not_allowed_tokens))
    
    return jsonify({'message': 'Usuario fez o logout com sucesso!'}), 200
    
def get_user_by_cpf(cpf):
    db = get_db()
    
    user = db.execute(
        'SELECT * FROM users WHERE cpf = ?', (cpf,)
    ).fetchone()
            
    return user


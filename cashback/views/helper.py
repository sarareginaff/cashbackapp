import cashback
import jwt
import werkzeug.security
import redis
import datetime
from flask import request, jsonify, current_app as app
from functools import wraps
from cashback.views import auth_route as auth

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
                
        r = redis.StrictRedis(host=app.config['REDIS_HOST'], 
                                port=app.config['REDIS_PORT'],
                                decode_responses=True)
        not_allowed_tokens = r.get('not_allowed_tokens')
        
        if not token:
            return jsonify({'message': 'Esta faltando o token'}), 401
        elif not_allowed_tokens and token in not_allowed_tokens:
            return jsonify({'message': 'Token nao esta habilitado. Usuario foi deslogado'}), 401
        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'])
            
            if data['exp'] < datetime.datetime.now().timestamp():
                return jsonify({'message': 'Token expirado'}), 401
            else:
                current_user = auth.get_user_by_cpf(cpf=data['cpf'])
        except:
            return jsonify({'message': 'Token invalido'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
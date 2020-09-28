import redis
import json
from werkzeug.security import generate_password_hash
from flask import current_app as app

from cashback.db.db import get_db


def get_user_by_cpf(cpf):
    db = get_db()
    
    user = db.execute(
        '''SELECT 
            id, 
            full_name, 
            cpf, 
            email, 
            password 
        FROM 
            users 
        WHERE 
            cpf = ?'''
        , (cpf,)
    ).fetchone()
            
    return user


def insert_new_user(full_name, cpf, email, password):
    db = get_db()
    
    db.execute(
        '''INSERT INTO 
            users 
        (
            full_name, 
            cpf, 
            email, 
            password
        ) 
        VALUES (?, ?, ?, ?)''',
        (full_name, cpf, email, generate_password_hash(password),)
    )
    
    db.commit()
    

def get_not_allowed_tokens():
    r = redis.StrictRedis(host=app.config['REDIS_HOST'], 
                            port=app.config['REDIS_PORT'],
                            decode_responses=True)
                            
    not_allowed_tokens = list(r.get('not_allowed_tokens'))
    
    r.connection_pool.disconnect()
    
    return not_allowed_tokens

    
def update_not_allowed_tokens(list):
    r = redis.StrictRedis(host=app.config['REDIS_HOST'], 
                            port=app.config['REDIS_PORT'],
                            decode_responses=True)
    
    r.set('not_allowed_tokens', json.dumps(list))
    
    r.connection_pool.disconnect()
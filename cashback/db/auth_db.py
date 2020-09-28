import redis
import json
from werkzeug.security import generate_password_hash
from flask import current_app as app

from cashback.db.db import get_db


def get_user_by_cpf(cpf):
    """
        Get user by cpf

        :Parameters: 
            - cpf (string): CPF of user responsible for purchase.

        :Returns: 
            - user (dict): user data

        :author: sarareginaff       
        :creation: Sep/2020
    """
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
    """
        Insert new user.

        :Parameters: 
            - full_name (string): Full name of new user
            - cpf (string): CPF of new user
            - email (string): email of new user
            - password (string): password of new user

        :author: sarareginaff       
        :creation: Sep/2020
    """
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
    """
        get list of not allowed tokens.

        :Returns: 
            - not_allowed_tokens (list): list of not allowed tokens

        :author: sarareginaff       
        :creation: Sep/2020
    """
    r = redis.StrictRedis(host=app.config['REDIS_HOST'], 
                            port=app.config['REDIS_PORT'],
                            decode_responses=True)

    not_allowed_tokens_str = r.get('not_allowed_tokens')
    if not_allowed_tokens_str: 
        not_allowed_tokens = list(json.loads(not_allowed_tokens_str))
    else:
        not_allowed_tokens = []
    
    r.connection_pool.disconnect()

    return not_allowed_tokens

    
def update_not_allowed_tokens(not_allowed_tokens):
    """
        update list of not allowed tokens.

        :Parameters: 
            - not_allowed_tokens (list): list of not allowed tokens

        :author: sarareginaff       
        :creation: Sep/2020
    """
    r = redis.StrictRedis(host=app.config['REDIS_HOST'], 
                            port=app.config['REDIS_PORT'],
                            decode_responses=True)

    r.set('not_allowed_tokens', json.dumps(not_allowed_tokens))
    
    r.connection_pool.disconnect()
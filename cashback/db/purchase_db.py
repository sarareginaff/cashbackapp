from cashback.db.db import get_db
from cashback.models import purchase_model


def insert_new_purchase(code, value, dth_purchase, cpf):
    """
        Insert new purchase.

        :Parameters: 
            - code (string): purchase code
            - value (number): purchase value
            - dth_purchase (string): date of purchase in format %Y-%m-%d %H:%M:%S
            - cpf (string): CPF of user responsible for purchase.

        :author: sarareginaff       
        :creation: Sep/2020
    """
    db = get_db()
    
    db.execute(
        '''INSERT INTO 
            purchases 
        (
            code, 
            value, 
            dth_purchase, 
            id_user, 
            id_status
        )
        VALUES (
            ?, 
            ?, 
            ?, 
            (SELECT id FROM users WHERE cpf = ?), 
            (SELECT id FROM purchase_status WHERE status_desc = ?)
        )''',
        (code, value, dth_purchase, cpf, purchase_model.define_purchase_status(cpf),)
    )
    
    db.commit()
    

def get_all_purchases():
    """
        Gets all purchases.

        :Returns: 
            - purchases (list): list of purchases with its code, value, dth_purchase, cpf and status

        :author: sarareginaff       
        :creation: Sep/2020
    """
    db = get_db()
    
    return db.execute(
        '''SELECT 
            p.code, 
            p.value, 
            p.dth_purchase, 
            u.cpf, 
            ps.status_desc 
        FROM 
            purchases p 
        JOIN 
            users u 
        ON 
            u.id = p.id_user 
        JOIN 
            purchase_status ps 
        ON 
            ps.id = p.id_status'''
    ).fetchall()

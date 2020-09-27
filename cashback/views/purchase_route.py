import functools
import sys
import requests
from requests.exceptions import HTTPError
from flask import (
    Blueprint, g, request, session, jsonify, current_app as app
)
from cashback.db.db import get_db
from cashback.views import helper
from cashback.models import purchase_model

bp = Blueprint('purchase', __name__, url_prefix='/purchase')


@bp.route('/register', methods=['POST'])
@helper.token_required
def register(current_user):
    try:
        code = request.json['code']
        value = request.json['value']
        dth_purchase = request.json['dth_purchase']
        cpf = request.json['cpf']
        
        status = "Validation"
        if(cpf in list(app.config['APPROVED_CPFS'])):
            status = "Approved"

        db = get_db()
        error = None
    
        if not code:
            error = 'Codigo da compra eh necessario. '
        if not value:
            error += 'Valor da compra eh necessario. '
        if not dth_purchase:
            error += 'Data da compra eh necessaria. '
        if not cpf:
            error += 'CPF do revendedor ou da revendedora eh necessaria. '

        if error is not None:
            return jsonify({'message': error}), 406
        elif db.execute(
                'SELECT id FROM users WHERE cpf = ?', (cpf,)
            ).fetchone() is None:
            return jsonify({'message': 'Esta pessoa nao esta cadastrada no sistema ainda. Favor realizar o cadastro'}), 406
    
        db.execute(
            'INSERT INTO purchases (code, value, dth_purchase, id_user, id_status) VALUES (?, ?, ?, (SELECT id FROM users WHERE cpf = ?), (SELECT id FROM purchase_status WHERE status_desc = ?))',
            (code, value, dth_purchase, cpf, status,)
        )
        db.commit()
        
        return jsonify({'message': 'Compra cadastrada com sucesso'}), 200
    except:
        return jsonify({'message': 'Nao foi possivel registrar a compra - {}'.format(sys.exc_info())}), 500
    
    
@bp.route('/listall', methods=['GET'])
@helper.token_required
def list_all(current_user):
    try:
        db = get_db()
        error = None
        purchases = db.execute(
            'SELECT p.code, p.value, p.dth_purchase, u.cpf, ps.status_desc FROM purchases p JOIN users u ON u.id = p.id_user JOIN purchase_status ps ON ps.id = p.id_status'
        ).fetchall()
    
        if purchases is None:
            return jsonify({'message': 'Nao ha compras cadastradas.'}), 401
        
        purchases_cashback = purchase_model.calculate_cashback(purchases)
        
        return jsonify({'message': 'Listagem de compras feita com sucesso', 
                        'data': purchases_cashback.to_dict(orient="records")}), 200
    except:
        return jsonify({'message': '[List All] Erro ao obter lista de compras e respectivos cashbacks - {}'.format(sys.exc_info())}), 500


@bp.route('/accumulatedcashback', methods=['GET'])
@helper.token_required
def get_accumulated_cashback(current_user):
     try:
         cpf = request.args.get('cpf')
         
         response = requests.get(
                                'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf={}'.format(cpf),
                                 headers={'token': '&#39;ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm&#39;'})
    
         response.raise_for_status()
     except HTTPError as http_err:
         return jsonify({'message': '[Get Accumulated Cashback] HTTP error occurred', 'exeption': http_err}), 500
     except Exception as err:
         return jsonify({'message': '[Get Accumulated Cashback] Erro ao obter cashback acumulado - {}'.format(err)}), 500
     else:
         return response.text


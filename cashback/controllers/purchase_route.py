import requests
from requests.exceptions import HTTPError
from flask import Blueprint, request, jsonify

from cashback.controllers import helper
from cashback.models import purchase_model, auth_model
from cashback.db import auth_db, purchase_db

bp = Blueprint('purchase', __name__, url_prefix='/purchase')


@bp.route('/register', methods=['POST'])
@helper.token_required
def register(current_user):
    try:
        code = request.json['code']
        value = request.json['value']
        dth_purchase = request.json['dth_purchase']
        cpf = auth_model.clean_cpf(request.json['cpf'])
        
        error = purchase_model.validate_purchase_register(code, value, dth_purchase, cpf)

        if error != '':
            return jsonify({'message': error}), 406
        elif auth_db.get_user_by_cpf is None:
            return jsonify({'message': 'Esta pessoa nao esta cadastrada no sistema ainda. Favor realizar o cadastro'}), 406
    
        purchase_db.insert_new_purchase(code, value, dth_purchase, cpf)
        
        return jsonify({'message': 'Compra cadastrada com sucesso'}), 200
    except Exception as err:
        return jsonify({'message': 'Nao foi possivel registrar a compra - {}'
                        .format(err)}), 500
    
    
@bp.route('/listall', methods=['GET'])
@helper.token_required
def list_all(current_user):
    try:
        purchases = purchase_db.get_all_purchases()

        if purchases is None:
            return jsonify({'message': 'Nao ha compras cadastradas.'}), 401
        
        purchases_cashback = purchase_model.calculate_cashback(purchases)
        
        return jsonify({'message': 'Listagem de compras feita com sucesso', 
                        'data': purchases_cashback.to_dict(orient="records")}), 200
    except Exception as err:
        return jsonify({'message': '[List All] Erro ao obter lista de compras e respectivos cashbacks - {}'
                        .format(err)}), 500


@bp.route('/accumulatedcashback', methods=['GET'])
@helper.token_required
def get_accumulated_cashback(current_user):
     try:
         cpf = auth_model.clean_cpf(request.args.get('cpf'))
         
         response = requests.get('https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf={}'.format(cpf),
                                 headers = {'token': '&#39;ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm&#39;'})
    
         response.raise_for_status()
     except HTTPError as http_err:
         return jsonify({'message': '[Get Accumulated Cashback] Ocorreu um erro de HTTP - {}'
                        .format(http_err)}), 500
     except Exception as err:
         return jsonify({'message': '[Get Accumulated Cashback] Erro ao obter cashback acumulado - {}'
                        .format(err)}), 500
     else:
         return response.text


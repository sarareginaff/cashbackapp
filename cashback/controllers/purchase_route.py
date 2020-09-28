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
    """
        Register new purchase.

        :Parameters: 
            - code (string): Code of purchase
            - value (number): value of purchase in reais
            - dth_purchase (string): date of purchase in format %Y-%m-%d %H:%M:%S
            - cpf (string): CPF of user responsible for purchase. Can have dots and hifens
        
        :Headers: 
            - Authorization (string): token of user.
            - Content-Type: application/json
        
        :Returns: 
            - message (string): Success if purchase is registered. Errors explanation if not

        :author: sarareginaff       
        :creation: Sep/2020
    """
    try:
        code = request.json['code']
        value = request.json['value']
        dth_purchase = request.json['dth_purchase']
        cpf = auth_model.clean_cpf(request.json['cpf'])
        
        error = purchase_model.validate_purchase_register(code, value, dth_purchase, cpf)

        if error != '':
            return jsonify({'message': error}), 406
        elif auth_db.get_user_by_cpf is None:
            return jsonify({'message': '''Esta pessoa nao esta cadastrada no sistema ainda.
                            Favor realizar o cadastro'''}), 406
    
        purchase_db.insert_new_purchase(code, value, dth_purchase, cpf)
        
        return jsonify({'message': 'Compra cadastrada com sucesso'}), 200
    except Exception as err:
        return jsonify({'message': 'Nao foi possivel registrar a compra - {}'
                        .format(err)}), 500
    
    
@bp.route('/listall', methods=['GET'])
@helper.token_required
def list_all(current_user):
    """
        List all purchases with calculated cashbacks.

        :Headers: 
            - Authorization (string): token of user.
            - Content-Type: application/json
        
        :Returns: 
            - message (string): Success if purchase is registered. Errors explanation if not
            - data (list): List of purchases with calculated cashbacks

        :author: sarareginaff       
        :creation: Sep/2020
    """
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
    """
        List accumulated cashbacks of user.

        :Parameters: 
            - cpf (string): CPF of user responsible for purchase. Can have dots and hifens

        :Headers: 
            - Authorization (string): token of user.
            - Content-Type: application/json
        
        :Returns: 
            - message (string): If there is some error
            - cpf (string): CPF of user
            - value (number): Accumulated cashbacks

        :author: sarareginaff       
        :creation: Sep/2020
    """
    try:
        cpf = auth_model.clean_cpf(request.args.get('cpf'))
        
        response = requests.get('https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf={}'
                                   .format(cpf),
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


# CashbackApp

Este repositório traz a base de um sistema de cálculo de cashback para revendedores. As premissas para cálculo do cashback são:

* Para até 1.000 reais em compras, será calculado 10% de cashback do
valor vendido no período de um mês;
* Entre 1.000 e 1.500 reais em compras, será calculado 15% de cashback do valor vendido no período de um mês;
* Acima de 1.500 reais em compras, será calculado 20% de cashback do valor vendido no período de um mês.

## Fazendo o sistema rodar

* Sugere-se criar um virtual environment 

```
python3 -m venv venv
source ./venv/bin/activate
```

* Utilizar os seguintes comandos na pasta raiz do repositório

```
pip3 install --editable .
```

  * Para ambiente de desenvolvimento:

```
export FLASK_APP=cashback
export FLASK_ENV=development
flask init-db
flask run
```

  * Caso contrário:

```
export FLASK_APP=cashback
flask init-db
flask run
```

## Funcionalidades

### Cadastro de novo usuário

Exige nome completo, CPF, e-mail e senha.

```
curl -X POST http://127.0.0.1:5000/auth/register -d '{"full_name": <full name>, "cpf": <cpf>, "email": <email>, "password": <password>}' -H "Content-Type: application/json"
```

### Login

Valida o login do usuário. Exige CPF e senha. Caso o login seja bem sucedido, um token é retornado para ser utilizado nas funções internas do sistema.

```
curl -X POST http://127.0.0.1:5000/auth/login -d '{"cpf": <cpf>, "password": <password>}' -H "Content-Type: application/json"
```

### Logout

Exige o token do usuário logado. Após efetuar o logout, o token ficará invalidado e o usuário só conseguirá utilizar o sistema novamente se realizar o login mais uma vez.

```
curl -X GET http://127.0.0.1:5000/auth/logout -H "Authorization:<token>"
```

### Cadastro de nova compra

Exige código da compra, valor da compra, data e CPF do usuário. A compra é cadastrada como 'Em Validação' a menos que o CPF do usuário esteja na lista de usuários autorizados a terem compras aprovadas automaticamente, ficando com status 'Aprovado'. 

Esta ação exige o token do usuário logado.

```
curl -X POST http://127.0.0.1:5000/purchase/register -d '{"code": <code>, "value": <value>, "dth_purchase": <YYYY-MM-DD HH-MM-SS>, "cpf": <cpf>}' -H "Content-Type: application/json" -H "Authorization:<token>"
```

### Listar todas as compras cadastradas

Exibirá todos os dados das compras, inclusive porcentagem e valor bruto de cashback aplicado a cada uma delas.

Esta ação exige o token do usuário logado.

```
curl -X GET http://127.0.0.1:5000/purchase/listall -H "Authorization:<token>"
```

### Exibir o valor acumulado de cashback para o usuário

Exibirá o valor em reais de cashback acumulado para o CPF especificado.

Esta ação exige o token do usuário logado.

```
curl -X GET http://127.0.0.1:5000/purchase/accumulatedcashback?cpf=123456 -H "Authorization:<token>"
```

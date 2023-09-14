from flask import request, jsonify, Flask
import json
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ручка, чтобы узнать список всех возможных валют
@app.route('/api/rates', methods=['GET'])
def get_rates():
    response = requests.get('https://open.er-api.com/v6/latest/AED').json()
    result = [rate for rate in response['rates']]
    return jsonify(", ".join(result)), 200

# ручка для конвертации валюты
@app.route('/api/convert', methods=['GET'])
def convert():
    convert_from = request.args.get('from')
    convert_to = request.args.get('to')
    amount = request.args.get('amount')
    print(convert_from)

    with open('static/errors.json', 'r', encoding='utf-8') as json_file:
        errors = json.load(json_file)

    # проверим, были ли заданы все необходимые параметры
    if not (convert_from and convert_to and amount):
        return jsonify(errors['not_all_parameters_given']), 400
    
    # проверка является ли заданная сумма валидным числом
    try:
        amount = float(amount)
    except:
        return jsonify(errors['not_a_number']), 400
    
    # если все хорошо, то делаем запрос к ExchangeRate-API и возвращаем ответ пользователю
    response = convert_value(convert_from, convert_to, amount, errors)
    return (response)


def convert_value(convert_from: str, convert_to: str, amount: float, errors):
    response = requests.get(f'https://open.er-api.com/v6/latest/{convert_from.upper()}').json() # отправим запрос к api
    if response['result'] == 'success':
        current_course = response.get('rates').get(f'{convert_to.upper()}')
        # обработка случая, когда валюта, в которую хотим конвертировать не валидна
        if not current_course:
            return jsonify(errors['no_such_currency_to_convert_to']), 400
        
        # если все хорошо, то конвертируем и возвращаем ответ
        result = amount * current_course
        return jsonify(f'You have converted {amount} {convert_from} to {round(result, 4)} {convert_to}'), 200
        
    # обработка случая, когда мы пытаемся конвертировать непонятную валюту
    else:
        response['message'] = 'You are trying to convert from non-exsisting currency. Visit https://www.exchangerate-api.com/docs/free to find out what currencies are available'
        return jsonify(response), 400

if __name__ == '__main__':
    app.run(debug=True)
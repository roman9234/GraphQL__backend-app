import jwt
from flask import jsonify

token = jwt.encode({
                                'uuid': uuid,
                                'username': username,
                                'expiration': str(datetime.utcnow() + timedelta(seconds=120))
                            },
                                app.config['SECRET_KEY'],
                                algorithm='HS256')

jsonify({'jwt_token': token})


def token_required(request, app):  # декоратор - если для выполнения действия нужен токен.
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):

            # получаем токен из сессии
            try:
                if request.method == 'POST' or request.method == 'PUT':
                    data = request.get_json()
                    token = data['jwt_token']
                if request.method == 'GET' or request.method == 'DELETE':
                    token = request.args.get('jwt_token')
            except:
                return jsonify({'status': 'unknown error'})
            if not token:
                return jsonify({'status': 'jwt_token is missing'})

            # проверяем токен
            try:
                # добавляем payload в аргументы функции
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                kwargs['payload'] = payload
            except jwt.exceptions.InvalidTokenError:
                return jsonify({'status': 'invalid jwt_token'})
            except:
                return jsonify({'status': 'unknown error'})
            return func(*args, **kwargs)

        return decorated

    return decorator




@app.route('/check_token', methods=['POST'])
@token_required(request, app)
def check_token(payload):
    return jsonify({'status':'success','payload': payload})










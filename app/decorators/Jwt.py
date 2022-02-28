
from flask import jsonify

from app import jwt


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return {'code': '305', 'status': 'error',
            'data': {'token': {'expired_token': 'The {} token has expired'.format(token_type)}}}


@jwt.invalid_token_loader
def my_invalid_token_callback(callback):
    return jsonify({'code': '305', 'status': 'error',
                    'data': {'token': {'invalid_token': callback}}})


@jwt.unauthorized_loader
def my_unauthorized_callback(callback):
    return jsonify({'code': '305', 'status': 'error',
                    'data': {'token': {'unauthorized': callback}}})

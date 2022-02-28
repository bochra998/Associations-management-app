from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from app.models.Users import Users


def check_permissions(permissions):
    def check_perm(List1, List2):
        check = False
        for m in List1:
            for n in List2:
                if m == n:
                    check = True
                    return check
        return check

    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth = get_jwt_identity()
            user = Users.find_by_email(auth)
            if user:
                uperms = user.get_permissions()
                if type(permissions) is list:
                    if not check_perm(uperms, permissions):
                        return {'code': '305', 'status': 'error',
                                    'data': {'permission': 'You don\'t have permission to access this endpoint'}}
                else:
                    if permissions not in uperms:
                        return {'code': '305', 'status': 'error',
                                'data': {'permission': 'You don\'t have permission to access this endpoint'}}
                return func(*args, **kwargs)
            else:
                return {'code': '305', 'status': 'error',
                            'data': {'user': 'Token doesn\'t exists'}}
        return wrapper

    return real_decorator

from typing import Any, Callable
import jwt
import os
from functools import wraps
from flask import request, jsonify

secret_key = os.environ.get('JWT_SECRET_KEY')

def verify_token(token):
    try:
        secret_key = os.environ.get('JWT_SECRET_KEY')
        secret_key = "8578d834f050ab9020f7e909799fc661b3457f43"
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    @wraps(func)
    def decorated(*args, **kwargs) -> Any:
        token = request.headers.get('Authorization', None)

        if not token:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        payload = verify_token(token)

        if not payload:
            return jsonify({'error': 'Token de autorização inválido ou expirado'}), 401
        
        return func(*args, **kwargs)

    return decorated
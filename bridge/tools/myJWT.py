import time
import jwt
from django.conf import settings


def make_token(user_id, expire = 3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now_time = time.time()
    payload_data = {'user_id': user_id, 'exp': now_time + expire}
    return jwt.encode(payload_data, key, algorithm='HS256')

def GetId(token):
    data = jwt.decode(
        jwt=token,
        key=settings.JWT_TOKEN_KEY,
        algorithms='HS256')
    return data

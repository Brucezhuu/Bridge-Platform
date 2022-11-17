import time
import jwt
from Bridge课程平台后端.settings import JWT_TOKEN_KEY


def make_token(user_id, expire=36000 * 24):
    key = JWT_TOKEN_KEY
    now_time = time.time()
    payload_data = {'user_id': user_id, 'exp': now_time + expire}
    return jwt.encode(payload_data, key, algorithm='HS256')


def GetId(token):
    data = jwt.decode(
        jwt=token,
        key=JWT_TOKEN_KEY,
        algorithms='HS256')
    return data


if __name__ == '__main__':
    en = make_token("222")
    print(type(en), en)
    print(GetId(en))


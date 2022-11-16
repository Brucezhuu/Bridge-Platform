import time
import jwt

SECRET_KEY = 'bruce*98f*8fr*vf8vf5'


def GetToken(id, username, auth):
    ADMIN_TOKEN_EXPIRE = 14 * 24 * 60 * 60
    now = int(time.time())
    token = jwt.encode(
        headers={
            'typ': 'jwt',
            'alg': 'HS256'
        },
        payload={
            'exp': now + ADMIN_TOKEN_EXPIRE,
            'iat': now,
            'data': {
                'id': id,
                'username': username,
                'auth': auth,
            }
        },
        key=SECRET_KEY,
        algorithm='HS256'
    )
    return token


def GetName(token):
    data = jwt.decode(
        jwt=token,
        key=SECRET_KEY,
        algorithms='HS256')
    print(data.get('data').get('id'))
    print(data.get('data').get('username'))

    return data


print('GetName: \n', GetName(GetToken(12, 'scorhl', 1)))

print('GetToken: \n', GetToken(12, 'scorhl', 1))

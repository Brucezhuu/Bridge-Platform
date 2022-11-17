import random
import hashlib

# def encode(pswd):
#     KEY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*(),.?[]{}-=+;:|"
#     salt = ''
#     for i in range(len(pswd)):
#         salt += random.choice(KEY)
#     return salt
#
#
# def check(input_str, store_str):
#     length = len(store_str) - 8
#     actual_p = store_str[2:length]
#     if not input_str == actual_p[::-1]:
#         return False
#     return True


if __name__ == '__main__':
    pswd = "123456"
    process = hashlib.md5()
    encode = process.update(pswd.encode("utf-8"))
    print(encode)

    encode = process.update(pswd.encode("utf-8"))
    print(encode)
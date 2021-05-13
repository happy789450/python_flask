import hashlib


def md5encrypt(str):
    h1 = hashlib.md5()
    h1.update(str.encode(encoding='utf-8'))
    return h1.hexdigest()

if __name__ == '__main__':
    result = md5encrypt('mypwd')
    print(result)
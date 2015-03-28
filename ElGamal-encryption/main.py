import client
import random

BASE_URL = 'http://pac.bouillaguet.info/TP3/ElGamal-encryption'

def XGCD(a, b):
    u = (1, 0)
    v = (0, 1)

    while(b != 0):
        q, r = divmod(a, b)
        a = b
        b = r
        tmp = (u[0] - q * v[0], u[1] - q * v[1])
        u = v
        v = tmp

    return a, u[0], u[1]

def modinv(a, b):
    g, x, y = XGCD(a, b)
    return x

if __name__ == '__main__':
    server = client.Server(BASE_URL)

    response = server.query('/parameters/sommerard')

    p = response['p']
    g = response['g']

    x = random.randint(1, p-1)

    # g^x mod p
    gx = pow(g, x, p)

    parameters = { 'h': gx }
    response = server.query('/challenge/sommerard', parameters)

    gy = response['ciphertext'][0]
    mgxy = response['ciphertext'][1]

    gxy = pow(gy, x, p)
    invgxy = modinv(gxy, p)

    m = (invgxy * mgxy) % p

    parameters = { 'plaintext': m }
    response = server.query('/validate/sommerard', parameters)
    print(response)

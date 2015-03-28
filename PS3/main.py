import client
import random

BASE_URL = 'http://pac.bouillaguet.info/TP3/PS3'

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

def sign(m):
    parameters = { 'm': m }
    response = server.query('/sign/sommerard', parameters)
    return response['signature'][0], response['signature'][1]

if __name__ == '__main__':
    server = client.Server(BASE_URL)

    response = server.query('/PK/sommerard')

    p = response['p']
    g = response['g']

    # h = g^x mod p
    h = response['h']
    q = p - 1

    m0 = 423424224
    r, s0 = sign(m0)
    m1 = 432423432243
    _, s1 = sign(m1)

    tmp, _, _ = XGCD(r, q)

    while(tmp != 1):
        response = server.query('/PK/sommerard/change')
        p = response['p']
        g = response['g']
        h = response['h']
        q = p - 1
        r, s0 = sign(m0)
        _, s1 = sign(m1)
        tmp, _, _ = XGCD(r, q)

    if((r >= 0) & (r < p) & (s0 >= 0) & (s0 < q)):
        gm0 = pow(g, m0, p)
        hr = pow(h, r, p)
        rs0 = pow(r, s0, p)
        print(gm0)
        print(((hr * rs0) % p))
        if(gm0 == ((hr * rs0) % p)):
            print('sign(m0) -> OK')
        else:
            print('sign(m0) -> FAIL')
    else:
        print('sign(m0) -> FAIL')

    if((r >= 0) & (r < p) & (s1 >= 0) & (s1 < q)):
        gm1 = pow(g, m1, p)
        hr = pow(h, r, p)
        rs1 = pow(r, s1, q)
        if(gm1 == ((hr * rs1) % q)):
            print('sign(m1) -> OK')
        else:
            print('sign(m1) -> FAIL')
    else:
        print('sign(m1) -> FAIL')

    tmp = modinv((s0 - s1), q)
    k = (((m0 - m1) * tmp) % q) # OK

    tmp = modinv(r, q)
    x = (((m0 - (k * s0)) * tmp) % q)

    if((k > 2) & (k < q-1)):
        print("(k > 2) & (k < q-1) -> OK")
    else:
        print("(k <= 2) || (k >= q-1) -> FAIL")

    tmp, _, _ = XGCD(k, q)
    if(tmp == 1):
        print("XGCD(k, q) == 1 -> OK")
    else:
        print("XGCD(k, q) != 1 -> FAIL")

    tmp1 = (r % p)
    tmp2 = pow(g, k, p)
    if(tmp1 == tmp2):
        print("r == g^k -> OK")
    else:
        print("r != g^k -> FAIL")

    tmp = ((m0 - (x * r)) * modinv(k, q)) % q
    if(tmp == s0):
        print("s == s0 -> OK")
    else:
        print("s != s0 -> FAIL")

    tmp = ((m1 - (x * r)) * modinv(k, q)) % q
    if(tmp == s1):
        print("s == s1 -> OK")
    else:
        print("s != s1 -> FAIL")

    if(h == pow(g, x, p)):
        print('okokokokok')

    parameters = { 'x': x }
    response = server.query('/validate/sommerard', parameters)
    print(response)

    """p = response['p']
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
    print(response)"""

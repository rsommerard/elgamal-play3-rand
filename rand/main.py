import client

BASE_URL = 'http://pac.bouillaguet.info/TP3/rand'

class Rand:
    def __init__(self):
        self.next = 1

    def rand(self):
        self.next = self.next * 1103515245 + 12345 % 2**32
        return (self.next // 2**16) % 2**15

    def srand(self, seed):
        self.next = seed

def bin_maker(a, b, c):
    p = 0
    p = a
    p = p<<15 | b
    p = p<<16 | c
    return p

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
    rand = Rand()

    server = client.Server(BASE_URL)

    response = server.query('/challenge/sommerard')

    IV = {}
    IV[0] = response['IV'][0]
    IV[1] = response['IV'][1]

    print("IV: " + str(IV))

    print('-' * 80)

    ########################################
    iv1 = []
    pred = 0
    for a in range(0, 2):
        for c in range(0, 2**16):
            pred = bin_maker(a, IV[0], c)
            rand.srand(pred)
            if(rand.rand() == IV[1]):
                iv1.append(pred)

    print("iv1: " + str(iv1))
    print('-' * 80)

    for i in iv1:
        rand.srand(i)
        print(str((i // 2**16) % 2**15) + " | " + str(rand.rand()))

    print('-' * 80)
    ########################################

    iv0 = []
    for i in iv1:
        inva = modinv(1103515245, 2**32)
        tmp = inva * (i - 12345) % 2**32
        iv0.append(tmp)

    print("iv0: " + str(iv0))
    print('-' * 80)

    for i in iv0:
        rand.srand(i)
        print(str((i // 2**16) % 2**15) + " | " + str(rand.rand()) + " | " + str(rand.rand()))

    print('-' * 80)
    ########################################

    key3 = []
    for i in iv0:
        inva = modinv(1103515245, 2**32)
        tmp = inva * (i - 12345) % 2**32
        key3.append(tmp)

    print("key3: " + str(key3))
    print('-' * 80)

    for i in key3:
        rand.srand(i)
        print(str((i // 2**16) % 2**15) + " | " + str(rand.rand()) + " | " + str(rand.rand()) + " | " + str(rand.rand()))

    print('-' * 80)
    ########################################

    key2 = []
    for i in key3:
        inva = modinv(1103515245, 2**32)
        tmp = inva * (i - 12345) % 2**32
        key2.append(tmp)

    print("key2: " + str(key2))
    print('-' * 80)

    for i in key2:
        rand.srand(i)
        print(str((i // 2**16) % 2**15) + " | " + str(rand.rand()) + " | " + str(rand.rand()) + " | " + str(rand.rand()) + " | " + str(rand.rand()))

    print('-' * 80)
    ########################################

    key1 = []
    for i in key2:
        inva = modinv(1103515245, 2**32)
        tmp = inva * (i - 12345) % 2**32
        key1.append(tmp)

    print("key1: " + str(key1))
    print('-' * 80)

    for i in key1:
        rand.srand(i)
        print(str((i // 2**16) % 2**15) + " | " + str(rand.rand()) + " | " + str(rand.rand()) + " | " + str(rand.rand()) + " | " + str(rand.rand()) + " | " + str(rand.rand()))

    print('-' * 80)
    ########################################

    key0 = []
    for i in key1:
        inva = modinv(1103515245, 2**32)
        tmp = inva * (i - 12345) % 2**32
        key0.append(tmp)

    print("key0: " + str(key0))
    print('-' * 80)

    rand.srand(key0[0])
    keys0 = [rand.rand(), rand.rand(), rand.rand(), rand.rand()]
    print(keys0)
    rand.srand(key0[1])
    keys1 = [rand.rand(), rand.rand(), rand.rand(), rand.rand()]

    parameters = { 'key': keys0 }
    response = server.query('/validation/sommerard', parameters)
    print(response)

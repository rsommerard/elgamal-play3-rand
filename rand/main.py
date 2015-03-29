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

def is_good_seed(seed, key, iv):
    srand(seed)
    key0 = rand()
    if(key0 == key[0]):
        print("key0 == key[0]")
        key1 = rand()
        if(key1 == key[1]):
            print("key1 == key[1]")
            key2 = rand()
            if(key2 == key[2]):
                print("key2 == key[2]")
                key3 = rand()
                if(key3 == key[3]):
                    print("key3 == key[3]")
                    iv0 = rand()
                    if(iv0 == iv[0]):
                        print("iv0 == iv[0]")
                        iv1 = rand()
                        if(iv1 == iv[1]):
                            print("iv1 == iv[1]")
                            return True

    return False

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
    ########################################

    for i in iv1:
        rand.srand(i)
        print(str((i // 2**16) % 2**15) + " | " + str(rand.rand()))

    iv0 = []
    for i in iv1:
        iv0.append(divmod((i - 12345), 1103515245))

    print(iv0)

    print(iv1[0])
    t = iv1[0] * 1103515245 + 12345
    print(t)
    n = divmod((t - 12345), 1103515245)
    print(n)


    """for i in iv1:
        srand(i)
        r = rand()
        print("i: " + str(i) + " | iv0: " + str((i // 65536) % 32768))
        print("i: " + str(i) + " | iv1: " + str(r))

    print('-' * 80)."""



    """key3 = search(iv0, iv[0])
    print("key3: " + str(key3))
    print('-' * 80)

    for i in key3:
        srand(i)
        print("i: " + str(i))
        print("rand1: " + str(rand()))
        print("rand2: " + str(rand()))

    key2 = search(key3, key[3])
    print("key2: " + str(key2))
    print('-' * 80)

    key1 = search(key2, key[2])
    print("key1: " + str(key1))
    print('-' * 80)

    key0 = search(key1, key[1])
    print("key0: " + str(key0))
    print('-' * 80)

    for seed in key0:
        if(is_good_seed(seed, key, iv)):
            print("Good seed: " + seed)
            break"""

import client

BASE_URL = 'http://pac.bouillaguet.info/TP3/rand'

next = 1

def rand():
    global next
    print('next0: ' + str(next) + ' | ' + bin(next))
    next = next * 1103515245 + 12345
    print('next1: ' + str(next) + ' | ' + bin(next))
    print('next2: ' + str((next // 65536) % 32768) + ' | ' + bin((next // 65536) % 32768))
    print('-' * 80)
    return (next // 65536) % 32768

def invrand(value):
    ret = (((value * 65536) - 12345) // 1103515245)
    print('ret: ' + str(ret) + ' | ' + bin(ret))
    print('-' * 80)
    return ret

def srand(seed):
    global next
    next = seed

if __name__ == '__main__':
    next = 1
    """server = client.Server(BASE_URL)

    response = server.query('/challenge/sommerard')
    print(response)

    IV[0] = response['IV'][0]
    IV[1] = response['IV'][1]

    print('IV[0]: ' + IV[0])
    print('IV[1]: ' + IV[1])

    print(rand)"""

    key = { 0: rand(), 1: rand(), 2: rand(), 3: rand() }
    iv = { 0: rand(), 1: rand() }

    print(key)
    print(iv)

    print(invrand(iv[1]))

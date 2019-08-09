from multiprocessing import Pool

from multiprocessing import Process, freeze_support

import time

def f(x):
    print('start:f()')
    print(x*x)
    while True:
        time.sleep(1)
        print('f()')
    print('end:f()')
    return x*x

def g(x):
    print('start:g()')
    print(x*x)
    while True:
        time.sleep(1)
        print('g()')
    print('end:g()')
    return x*x

MASTER_SERVER_DECLARING_PORT = 5007

DEFAULT_HOSTING_A_SERVER_PORT = 5008

if __name__ == '__main__':
    Process(target=f,args=(5,)).start()
    Process(target=g,args=(5,)).start()

    # with Pool(5) as p:
    #     print(p.map(f, [1, 2, 3]))
    #     p.map()

    # kill()
    # Same as terminate()

    # p.start()
    # p.join()
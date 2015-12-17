import os
import random
os.sys.path.append('/home/anton/edu/asymcrypt')

from fractions import gcd

import requests

from lab3 import (
    RANDOM_RANGE,
    URL_API_GETKEY,
    URL_API_CHALLENGE,
)


def attack(session, n):
    t = random.randint(*RANDOM_RANGE)
    y = pow(t, 2, n)
    print("Start request with parameter t = {} ...".format(t))
    result = session.get(URL_API_CHALLENGE, params={'y': hex(y)[2:]})
    status_code = result.status_code
    if status_code != 200:
        print("Request was not successful. Returned with status code: {}". format(status_code))
        return
    z = int(result.json()['root'], 16)
    print("Request was successful. z = {}".format(z))
    if z != t:
        p = gcd(t + z, n)
        q = n // p
        return p, q
    


def main():
    with requests.Session() as session:
        print("Start initial modulus request ...")
        initial_response = session.get(URL_API_GETKEY)
        status_code = initial_response.status_code
        if status_code != 200:
            print("Request was not successful. Returned with status code: {}". format(status_code))
            return
        n = int(initial_response.json()['modulus'], 16)
        print("Request was successful. n = {}".format(n))
        counter = 0
        while True:
            counter += 1
            result = attack(session, n)
            if result:
                p, q = result
                print("Attack #{} was successful".format(counter))
                print("p = {}, q = {}".format(p, q))
                break
            print("Attack #{} was not successful".format(counter))


if __name__ == '__main__':
    main()

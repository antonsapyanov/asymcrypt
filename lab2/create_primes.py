import os
os.sys.path.append('/home/anton/edu/asymcrypt')

from lab2 import (
    N0,
    N1,
    PRIMES_AMOUNT,
    PATH_PRIMES_A,
    PATH_PRIMES_B,
)
from util import get_prime_number, write_primes

PATHES = (
    PATH_PRIMES_A,
    PATH_PRIMES_B,
)


def main():
    primes = []
    i = 0
    while i < PRIMES_AMOUNT:
        prime, time = get_prime_number(N0, N1)
        print("Prime #{}: {} sec(s)" .format(i+1, time))
        primes.append(prime)
        i += 1
    write_primes(primes, PATHES)


if __name__ == '__main__':
    main()

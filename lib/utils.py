import time

from functools import reduce


to_bits = lambda x: list(map(int, bin(x)[2:]))
to_number = lambda x: int("".join(map(str, reversed(x))), 2)


def lfsr(state, coefs, length):
    while True:
        mults = coefs & state
        bit = reduce(lambda x, y: x ^ y, to_bits(mults))
        state = (state >> 1) | (bit << (length - 1))
        yield bit


def timer(function):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        time_delta = time.time() - start
        return result, time_delta
    return wrapper


def get_d_and_s(n):
    s = 0
    for bit in reversed(to_bits(n)):
        if bit:
            break
        s += 1
    return n // 2**s, s


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - int(b / a) * y, y)


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

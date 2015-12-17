import configparser
import math
import random
from lab1.util import get_generators
from lab2 import (
    BITS_AMOUNT,
    GENERATOR_NAME,
    PATH_GENERATORS,
    SALT_RANGE,
)
from lib.tests import miller_rabin_primality_test as is_prime, timer
from lib.utils import to_number, modinv


@timer
def get_prime_number(n0, n1):
    gen = _get_generator(GENERATOR_NAME)(random.randint(*SALT_RANGE))
    while True:
        x = _generate_init_number(gen, BITS_AMOUNT)
        while not (n0 <= x <= n1):
            x = _generate_approp_number(gen, x, BITS_AMOUNT)
        prime_number = _get_prime_number(x, n1)
        if prime_number:
            return prime_number


def _get_generator(generator_name):
    return get_generators(PATH_GENERATORS)[generator_name]


def _generate_init_number(generator, amount):
    i = 0
    bits = []
    while i < amount:
        bits.append(next(generator))
        i += 1
    return to_number(bits)


def _generate_approp_number(generator, number, length):
    return (number >> 1) | (next(generator) << (length - 1))


def _get_prime_number(x, n1):
    m0 = x if x % 2 else x + 1
    for i in range(math.floor((n1 - m0)/2) + 1):
        number = m0 + 2*i
        if is_prime(number):
            return number


def write_primes(primes, pathes):
    sorted_primes = sorted(primes)
    configs = _get_configs(len(pathes))
    for i, config in enumerate(configs):
        _write_primes_to_config(sorted_primes[i:i+2], pathes[i], config)


def _get_configs(quantity):
    configs = []
    for _ in range(quantity):
        config = configparser.ConfigParser()
        config['primes'] = {}
        configs.append(config)
    return configs


def _write_primes_to_config(primes, filename, config):
    with open(filename, 'w') as configfile:
        p, q = primes
        config['primes']['p'] = str(p)
        config['primes']['q'] = str(q)
        config.write(configfile)


def get_primes(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config['primes'].getint('p'), config['primes'].getint('q')


def generate_keys(e, p, q):
    n = p * q
    d = modinv(e, n)
    return e, d, n


def write_keys(publicfile, privatefile, e, d, n):
    _write_keys(publicfile, 'e', e, n)
    _write_keys(privatefile, 'd', d, n)


def _write_keys(path, key_type, key_value, n):
    with open(path, 'w') as configfile:
        config = configparser.ConfigParser()
        config['keys'] = {}
        config['keys'][key_type] = str(key_value)
        config['keys']['n'] = str(n)
        config.write(configfile)

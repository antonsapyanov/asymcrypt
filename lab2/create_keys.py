import os
os.sys.path.append('/home/anton/edu/asymcrypt')

from lab2 import (
	PATH_PRIMES_A,
	PATH_PRIMES_B,
	PATH_PRIVATE_KEY_A,
	PATH_PRIVATE_KEY_B,
	PATH_PUBLIC_KEYS_A,
	PATH_PUBLIC_KEYS_B,
	E,
)
from lab2.util import get_primes, generate_keys, write_keys

PATHES = (
	(PATH_PRIMES_A, PATH_PUBLIC_KEYS_A, PATH_PRIVATE_KEY_A),
	(PATH_PRIMES_B, PATH_PUBLIC_KEYS_B, PATH_PRIVATE_KEY_B),
)


def main():
	for source, pub_target, priv_target in PATHES:
		p, q = get_primes(source)
		e, d, n = generate_keys(E, p, q)
		write_keys(pub_target, priv_target, e, d, n)


if __name__ == '__main__':
	main()

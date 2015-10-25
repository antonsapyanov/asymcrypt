import random

from functools import partial

__all__ = ['test_builtin_byte', 'builtin_byte']


def builtin_byte(init, min_, max_):
	random.seed(init)
	pseudo_rand_gen = partial(random.randint, min_, max_)
	while True:
		yield pseudo_rand_gen()


test_builtin_byte = builtin_byte

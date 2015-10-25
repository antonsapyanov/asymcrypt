import time

from functools import reduce


bits = lambda x: list(map(int, bin(x)[2:]))


def lfsr(state, coefs, length):
	while True:
		mults = coefs & state
		bit = reduce(lambda x, y: x ^ y, bits(mults))
		state = (state >> 1) | (bit << (length - 1))
		yield bit


def pow_mod(value, pow_, mod):
	bit_pow = bits(pow_)
	result = 1
	for bit in reversed(bit_pow):
		if bit:
			result = (result * value) % mod
		else:
			value = (value * value) % mod
	return result


def timer(function):
	def wrapper(*args, **kwargs):
		start = time.time()
		result = function(*args, **kwargs)
		time_delta = time.time() - start
		return result, time_delta
	return wrapper

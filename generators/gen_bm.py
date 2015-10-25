from lib.utils import pow_mod

__all__ = ['test_bm_bit', 'test_bm_byte', 'bm_bit', 'bm_byte']


def bm_bit(t, a, p):
	threshold = (p - 1) / 2
	while True:
		yield 1 if t < threshold else 0
		t = pow_mod(a, t, p)


def bm_byte(t, a, p):
	k = 0
	coef = (p - 1) / 256
	while True:
		while True:
			if k*coef < t <= (k+1)*coef:
				break
			k += 1
		yield k
		t = pow_mod(a, t, p)
		k = 0



test_bm_bit = bm_bit
test_bm_byte = bm_byte

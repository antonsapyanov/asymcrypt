from lib.utils import pow_mod

__all__ = ['test_bbs_bit', 'test_bbs_byte', 'bbs_bit', 'bbs_byte']


def bbs(r, p, q):
	n = p * q
	while True:
		r = pow_mod(r, 2, n)
		yield r


def bbs_bit(r, p, q):
	for r in bbs(r, p, q):
		yield r % 2


def bbs_byte(r, p, q):
	for r in bbs(r, p, q):
		yield r % 256


test_bbs_bit = bbs_bit
test_bbs_byte = bbs_byte

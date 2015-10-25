from lib.utils import lfsr

__all__ = ["test_jiffy", "jiffy"]


def jiffy(lsfr1_data, lsfr2_data, lsfr3_data):
	lfsr1 = lfsr(*lsfr1_data)
	lfsr2 = lfsr(*lsfr2_data)
	lfsr3 = lfsr(*lsfr3_data)
	while True:
		x = next(lfsr1)
		y = next(lfsr2)
		s = next(lfsr3)
		yield (s * x) ^ ((1 ^ s) * y)


def test_jiffy(x, coefs1, length1, coefs2, length2, coefs3, length3):
	#   x - is a dummy
	init_data = (
		(x, coefs1, length1),
		(x, coefs2, length2),
		(x, coefs3, length3),
	)
	yield from jiffy(*init_data)

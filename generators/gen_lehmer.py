__all__ = [
	"test_lehmer_high_byte", 
	"test_lehmer_low_byte", 
	"lehmer_high_byte", 
	'lehmer_low_byte'
]


def lehmer(x, a, m, c):
	while True:
		x = (a * x + c) % m
		yield x


def lehmer_low_byte(x, a, m, c):
	for xn in lehmer(x, a, m, c):
		yield xn & 255


def lehmer_high_byte(x, a, m, c):
	p = m.bit_length() - 1
	for xn in lehmer(x, a, m, c):
		yield xn >> (p - 8 if p > 8 else 0)


test_lehmer_low_byte = lehmer_low_byte
test_lehmer_high_byte = lehmer_high_byte

__all__ = ['test_librarian_byte', 'librarian_byte']

BYTES_LEN = 4096


def librarian_byte(path):
	with open(path, 'r', encoding='utf-8') as f:
		while True:
			bytes_ = bytes(f.read(BYTES_LEN), 'utf-8')
			for byte in bytes_:
				yield byte
			if len(bytes_) < BYTES_LEN:
				break


def test_librarian_byte(x, path):
	#	x - is a dummy
	yield from librarian_byte(path)

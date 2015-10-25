import random
import os
os.sys.path.append('/home/anton/dev/python/asymcrypt')

from lab1 import (
  MAX_RAND_INT,
  MIN_RAND_INT,
  PATH_GENERATORS, 
  PATH_SEQUENCES,
  PATH_TEST_RESULTS,
  SEQUENCE_LENGTH
)
from util import get_generators, write_sequence


def create_sequences(generators, path):
    for gn, gf in generators.items():
        randint = random.randint(MIN_RAND_INT, MAX_RAND_INT)
        seq_path = os.path.join(path, "{}.{}".format(gn, 'txt'))
        write_sequence(
            gf,
            randint,
            seq_path,
            SEQUENCE_LENGTH,
            'byte' if gn.endswith('_byte') else 'bit'
        )


def main():
    generators = get_generators(PATH_GENERATORS)
    create_sequences(generators, PATH_SEQUENCES)


if __name__ == '__main__':
    main()

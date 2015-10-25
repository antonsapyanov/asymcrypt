import os
os.sys.path.append('/home/anton/dev/python/asymcrypt')

from lab1 import (
    ALFAS,
    PATH_GENERATORS, 
    PATH_SEQUENCES,
    PATH_TEST_RESULTS,
    RS,
    SEQUENCE_LENGTH,
)
from lib.tests import (
    condition_of_character_equability,
    condition_of_character_independence,
    condition_of_character_uniformity,
)
from util import get_sequences, write_test_results


def test(sequences, path):
    for gn, sequence in sequences.items():
        res_path = os.path.join(path, "{}.{}".format(gn, 'txt'))

        eq_res, eq_time = condition_of_character_equability(sequence, SEQUENCE_LENGTH, ALFAS)
        write_test_results(eq_res, eq_time, res_path, 'equability')

        ind_res, ind_time = condition_of_character_independence(sequence, SEQUENCE_LENGTH, ALFAS)
        write_test_results(ind_res, ind_time, res_path, 'independence')
        
        uni_res, uni_time = condition_of_character_uniformity(sequence, SEQUENCE_LENGTH, ALFAS, RS)
        write_test_results(uni_res, uni_time, res_path, 'uniformity')


def main():
    sequences_dict = {gname: sequence for gname, sequence in get_sequences(PATH_SEQUENCES)}
    test(sequences_dict, PATH_TEST_RESULTS)


if __name__ == '__main__':
    main()
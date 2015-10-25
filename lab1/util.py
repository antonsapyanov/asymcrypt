import configparser
import os

from collections import defaultdict, OrderedDict
from functools import partial
from importlib import import_module

from lab1 import SEPARATOR
from lib.utils import timer

__all__ = [
    'get_generators', 
    'write_sequence', 
    'get_sequences', 
    'write_test_results'
]


def get_generators(path):
    raw_generators = {}
    parameters = None
    for entry in os.scandir(path):
        if entry.name.startswith('gen_'):
            for gn, gf in _get_generators_from_module(entry.name[:-3]):
              raw_generators[gn] = gf
        elif entry.name.startswith('init'):
            parameters = _get_parameters(entry.path)
    return {gn: partial(gf, **parameters.get(gn, {})) for gn, gf in raw_generators.items()}


def _get_generators_from_module(mod_name):
    module = import_module('generators.{module_name}'.format(module_name=mod_name))
    for name in module.__all__:
        if name.startswith('test_'):
            yield name[5:], getattr(module, name)


def _get_parameters(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    parameters = defaultdict(dict)
    for section in config.sections():
        for k, v in config.items(section):
            if v.startswith('0x'):
                parameters[section][k] = int(v, 16)
            elif v.isdigit():
                parameters[section][k] = int(v)
            else:
                parameters[section][k] = v
    return parameters


def write_sequence(generator_func, init_state, path, length, type_):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('Init state: {init_state}\n'.format(init_state=init_state))
        generator = generator_func(init_state)
        if type_ == 'bit':
            res, time = _write_bits(f, generator, length)
        elif type_ == 'byte':
            res, time = _write_bytes(f, generator, length)
        f.write("\nTotal time: {time} second(s)".format(time=time))


@timer
def _write_bits(f, generator, length):
    for _ in range(length):
        byte = [str(next(generator)) for _ in range(8)]
        f.write("{}{}".format(str(int(''.join(byte), 2)), SEPARATOR))


@timer
def _write_bytes(f, generator, length):
    for _ in range(length):
        f.write("{}{}".format(str(next(generator)), SEPARATOR))


def get_sequences(path):
    for entry in os.scandir(path):
        yield entry.name.split('.')[0], _get_sequence_from_file(entry.path)


def _get_sequence_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == 1:
                return list(map(int, line[:-2].split(SEPARATOR)))


def write_test_results(result, time, path, type_):
    with open(path, 'a', encoding='utf-8') as f:
        if type_ == 'equability':
            _write_equability_test_result(f, result, time)
        elif type_ == 'independence':
            _write_independence_test_result(f, result, time)
        elif type_ == 'uniformity':
            _write_uniformity_test_result(f, result, time)


def _write_equability_test_result(f, results, time):
    f.write('--- EQUABILITY TEST ---\n')
    for i, result in enumerate(results, 1):
        ord_result = OrderedDict(sorted(result.items(), key=lambda x: x[0]))
        f.write('%d)' % i)
        for res_name, res_value in ord_result.items():
            f.write("\t{name}: {value}\n".format(name=res_name, value=res_value))
    f.write('Time: {}  second(s)\n'.format(time))


def _write_independence_test_result(f, results, time):
    f.write('--- INDEPENDENCE TEST ---\n')
    for i, result in enumerate(results, 1):
        ord_result = OrderedDict(sorted(result.items(), key=lambda x: x[0]))
        f.write('%d)' % i)
        for res_name, res_value in ord_result.items():
            f.write("\t{name}: {value}\n".format(name=res_name, value=res_value))
    f.write('Time: {}  second(s)\n'.format(time))


def _write_uniformity_test_result(f, results, time):
    f.write('--- UNIFORMITY TEST ---\n')
    for i, alfa_results in enumerate(results, 1):
        for j, result in enumerate(alfa_results, 1):
            ord_result = OrderedDict(sorted(result.items(), key=lambda x: x[0]))
            f.write('%d.%d)' % (i, j))
            for res_name, res_value in ord_result.items():
                f.write("\t{name}: {value}\n".format(name=res_name, value=res_value))
    f.write('Time: {}  second(s)\n'.format(time))

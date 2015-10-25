import math

from collections import defaultdict
from functools import reduce

from .utils import timer

__all__ = [
	'condition_of_character_equability',
	'condition_of_character_independence',
	'condition_of_character_uniformity',
]

Z = {
	0.99: 0.83891293878626816,
	0.95: 0.82894388796634644,
	0.9: 0.81593990850046572,
}


def _get_expected_statistic(one_minus_alfa, l):
	assert one_minus_alfa in Z.keys()
	return math.sqrt(2 * l) * Z[one_minus_alfa] + l


@timer
def condition_of_character_equability(sequence, length, alfas):

	def get_results(statistic, alfas, l, length):
		results = []
		for alfa in alfas:
			expected_statistic = _get_expected_statistic(1 - alfa, l)
			results.append({
				'Result': statistic <= expected_statistic, 
				'Statistic': statistic, 
				'Expected statistic': expected_statistic,
				'alfa': alfa,
				'Sequnce length': length
			})
		return results

	frequency = defaultdict(int)
	expected_frequency = length / 256
	l = 255

	for byte in sequence:
		frequency[byte] += 1

	statistic = reduce(
		lambda x, y: x + (pow((frequency[y] - expected_frequency), 2) / expected_frequency), 
		range(256), 
		0
	)

	return get_results(statistic, alfas, l, length)


@timer
def condition_of_character_independence(sequence, length, alfas):

	def get_results(statistic, alfas, l, length):
		results = []
		for alfa in alfas:
			expected_statistic = _get_expected_statistic(1 - alfa, l)
			results.append({
				'Result': statistic <= expected_statistic, 
				'Statistic': statistic, 
				'Expected statistic': expected_statistic,
				'alfa': alfa,
				'Sequnce length': length
			})
		return results

	frequency = defaultdict(int)
	v = defaultdict(int)
	a = defaultdict(int)
	n = math.floor(length / 2)
	l = pow(255, 2)

	for i in range(n):
		frequency[(sequence[2*i], sequence[2*i + 1])] += 1
		v[sequence[2*i]] += 1
		a[sequence[2*i + 1]] += 1

	statistic = _count_statistic(n, 256, frequency, v, a)

	return get_results(statistic, alfas, l, length)


@timer
def condition_of_character_uniformity(sequence, length, alfas, rs):
	return [_condition_of_character_uniformity_for_r(sequence, length, alfas, r) for r in rs]


def _condition_of_character_uniformity_for_r(sequence, length, alfas, r):

	def get_results(statistic, alfas, l, length, r):
		results = []
		for alfa in alfas:
			expected_statistic = _get_expected_statistic(1 - alfa, l)
			results.append({
				'Result': statistic <= expected_statistic, 
				'Statistic': statistic, 
				'Expected statistic': expected_statistic,
				'r': r, 
				'alfa': alfa,
				'Sequnce length': length
			})
		return results

	frequency = defaultdict(int)
	v = defaultdict(int)
	a = {}
	m_ = math.floor(length / r)
	n = m_ * r
	l = 255 * (r - 1)

	for i in range(m_):
		for byte_ in sequence[r*i:r*(i+1)]:
			frequency[(byte_, i)] += 1
			v[byte_] += 1
	for j in range(r):
		a[j] = m_ 

	statistic = _count_statistic(n, r, frequency, v, a)

	return get_results(statistic, alfas, l, length, r)


def _count_statistic(n, r, f, v, a):

	def count(i, j):
		return pow(f[(i, j)], 2) / (v[i] * a[j]) if v[i] and a[j] else 0

	sum_ = reduce(
		lambda x, i: x + reduce(
			lambda y, j: y + count(i, j),
			range(r),
			0
		),
		range(256),
		0
	)

	return n * (sum_ - 1)

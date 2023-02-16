from core import FreqOracleClient

import numpy as np
import math
import random

class PrivSketchClient(FreqOracleClient):
    def __init__(self, epsilon, hash_funcs, m, d, is_hadamard=False, index_mapper=None):
        super().__init__(epsilon, None, index_mapper)
        self.sketch_based = True
        self.is_hadamard = is_hadamard
        self.d = d
        self.update_params(hash_funcs, m, epsilon)

        self.domain = np.arange(0, self.d, 1)
        self.n_hash = np.arange(0, self.k, 1)
        self.hash_index = np.array([[self.hash_funcs[i](str(v)) for v in self.domain] for i in self.n_hash])

    def update_params(self, hash_funcs=None, m=None, epsilon=None, index_mapper=None):
        if hash_funcs is not None:
            self.hash_funcs = hash_funcs
            self.k = len(self.hash_funcs)

        self.epsilon = epsilon if epsilon is not None else self.epsilon
        self.m = m if m is not None else self.m

        if epsilon is not None:
            self.prob = 1 / (1 + math.pow(math.e, self.epsilon))

    def _hash(self, data):
        v = np.full((self.k, self.m), -1)
        for d in data:
            for j in range(self.k):
                v[j][self.hash_index[j][self.index_mapper(d)]] = 1
        return v

    def _perturb(self, data):
        v = self._hash(data)
        o = self._generate_ordering_matrix(v)

        k_sample = random.randint(0, self.k - 1)
        m_sample = random.randint(0, self.m - 1)

        np.random.seed()
        r = np.random.random()
        if r < self.prob:
            v[k_sample][m_sample] *= -1

        return v[k_sample][m_sample], o, k_sample, m_sample

    def _generate_ordering_matrix(self, v):
        o = np.full((self.k, self.m), 0)

        minus_count = np.sum(v == -1)
        one_count = np.sum(v == 1)

        if minus_count != 0:
            minus_index = list(zip(np.where(v == -1)[0], np.where(v == -1)[1]))
            minus_index_permutation = np.random.permutation(np.array(minus_index))
            minus_transpose = minus_index_permutation.transpose()
            o[minus_transpose[0], minus_transpose[1]] = np.arange(0, minus_count, 1)

        if one_count != 0:
            one_index = list(zip(np.where(v == 1)[0], np.where(v == 1)[1]))
            one_index_permutation = np.random.permutation(np.array(one_index))
            one_transpose = one_index_permutation.transpose()
            o[one_transpose[0], one_transpose[1]] = np.arange(minus_count, self.k * self.m, 1)

        return o

    def privatise(self, data):
        return self._perturb(data)
from core import FreqOracleClient

import numpy as np
import math

class MultiPCMSMinClient(FreqOracleClient):
    def __init__(self, epsilon, hash_funcs, m, d, is_hadamard=False):
        super().__init__(epsilon, None)
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
            self.prob = 1 / (1 + math.pow(math.e, self.epsilon / (self.k * self.m)))

    def _hash(self, data):
        v = np.full((self.k, self.m), -1)
        for d in data:
            for j in range(self.k):
                h_j = self.hash_funcs[j]
                v[j][h_j(str(d))] = 1
        return v

    def _perturb(self, data):
        v = self._hash(data)
        np.random.seed()
        r = np.random.rand(*v.shape)
        v[r < self.prob] *= -1 # "flip" bits with prob
        return v

    def privatise(self, data):
        return self._perturb(data)
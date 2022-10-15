from core import FreqOracleClient

import numpy as np
import math
import random

class MultiPCMSMeanClient(FreqOracleClient):
    def __init__(self, epsilon, hash_funcs, m, is_hadamard=False):
        super().__init__(epsilon, None)
        self.sketch_based = True
        self.is_hadamard = is_hadamard
        self.update_params(hash_funcs, m, epsilon)

    def update_params(self, hash_funcs=None, m=None, epsilon=None, index_mapper=None):
        if hash_funcs is not None:
            self.hash_funcs = hash_funcs
            self.k = len(self.hash_funcs)

        self.epsilon = epsilon if epsilon is not None else self.epsilon
        self.m = m if m is not None else self.m

        if epsilon is not None:
            if self.is_hadamard:
                self.prob = 1 / (1 + math.pow(math.e, self.epsilon))
            else:
                self.prob = 1 / (1 + math.pow(math.e, self.epsilon / self.m))

    def _one_hot(self, data):
        j = random.randint(0, self.k-1)
        h_j = self.hash_funcs[j]
        v = [0] * self.m if self.is_hadamard else np.full(self.m, -1)
        for i in range(len(data)):
            v[h_j(str(data[i]))] = 1
        return v, j

    def _perturb(self, data):
        v, j = self._one_hot(data)  # modify the encode, and self.prob
        np.random.seed()
        r = np.random.rand(*v.shape)
        v[r < self.prob] *= -1 # "flip" bits with prob
        return v, j

    def privatise(self, data):
        return self._perturb(data)
from core import FreqOracleClient

import numpy as np
import math
import random

class nPCMSClient(FreqOracleClient):
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
                self.prob = 1 / (1 + math.pow(math.e, self.epsilon / 78 / 2))

    def _one_hot(self, data):
        j = random.randint(0, self.k-1)
        h_j = self.hash_funcs[j]
        v = [0] * self.m if self.is_hadamard else np.full(self.m, -1)
        v[h_j(data)] = 1
        return v, j

    def _perturb(self, data):
        vlist = []
        jlist = []
        for i in range(len(data)):
            v, j = self._one_hot(data)
            np.random.seed()
            r = np.random.rand(*v.shape)
            v[r < self.prob] *= -1 # "flip" bits with prob
            vlist.append(v)
            jlist.append(j)
        for i in range(78-len(data)):
            j = random.randint(0, self.k - 1)
            v = np.full(self.m, -1)
            r = np.random.rand(*v.shape)
            v[r < self.prob] *= -1 # "flip" bits with prob
            vlist.append(v)
            jlist.append(j)
        return vlist, jlist

    def privatise(self, data):
        return self._perturb(data)
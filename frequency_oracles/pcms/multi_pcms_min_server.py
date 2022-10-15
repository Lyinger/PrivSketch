
from core import FreqOracleServer
import math
import numpy as np
from core import generate_hash_funcs

class MultiPCMSMinServer(FreqOracleServer):
    def __init__(self, epsilon, k, m, d, estimation_items_num, is_hadamard=False, index_mapper=None):
        super().__init__(epsilon, d, index_mapper)
        self.sketch_based = True
        self.is_hadamard = is_hadamard
        self.update_params(k, m, epsilon, index_mapper=None)
        self.hash_funcs = generate_hash_funcs(k,m)
        self.estimation_num = estimation_items_num

        self.last_estimated = self.n
        self.ones = np.ones((self.k, self.m))

    def update_params(self, k=None, m=None, epsilon=None, index_mapper=None):
        self.k = k if k is not None else self.k
        self.m = m if m is not None else self.m
        self.hash_funcs = generate_hash_funcs(self.k,self.m)
        super().update_params(epsilon=epsilon, index_mapper=index_mapper) # This also calls reset() to reset sketch size
        if epsilon is not None:
            self.c = (math.pow(math.e, epsilon / (self.k * self.m)) + 1) / (math.pow(math.e, epsilon / (self.k * self.m)) - 1)

    def _add_to_sketch(self, data):
        self.sketch_matrix = self.sketch_matrix + ((self.c / 2) * data + 0.5 * self.ones)

    def _update_estimates(self):
        if self.is_hadamard:
            self.last_estimated = self.n # TODO: Is this needed?
            self.transformed_matrix = self._transform_sketch_matrix()

    def get_hash_funcs(self):
        return self.hash_funcs

    def reset(self):
        super().reset()
        self.sketch_matrix = np.zeros((self.k, self.m))
        self.transformed_matrix = np.zeros((self.k, self.m))

    def aggregate(self, data):

        self._add_to_sketch(data)
        self.n += 1

    def estimate(self, data, suppress_warnings=False):
        self.check_warnings(suppress_warnings)
        self.check_and_update_estimates()

        sketch = self.sketch_matrix if not self.is_hadamard else self.transformed_matrix

        data = str(data)
        k, m = sketch.shape
        freq_sum = []
        for i in range(0, k):
            freq_sum.append(sketch[i][self.hash_funcs[i](data)])

        return np.min(freq_sum)

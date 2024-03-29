from core import FreqOracleServer
import math
import numpy as np
from scipy.linalg import hadamard
from core import generate_hash_funcs

class PrivSketchServer(FreqOracleServer):
    def __init__(self, epsilon, k, m, d, estimation_items_num, is_hadamard=False, index_mapper=None):
        super().__init__(epsilon, d, index_mapper)
        self.sketch_based = True
        self.is_hadamard = is_hadamard
        self.update_params(k,m, epsilon, index_mapper=None)
        self.hash_funcs = generate_hash_funcs(k, m)

        self.estimation_num = estimation_items_num
        self.domain = np.arange(0, self.estimation_num, 1)
        self.n_hash = np.arange(0, self.k, 1)
        self.hash_index = np.array([[self.hash_funcs[i](str(v)) for v in self.domain] for i in self.n_hash])

        self.last_estimated = self.n
        self.ones = np.ones(self.d)

    def update_params(self, k=None, m=None, epsilon=None, index_mapper=None):
        self.k = k if k is not None else self.k
        self.m = m if m is not None else self.m
        self.hash_funcs = generate_hash_funcs(self.k,self.m)
        super().update_params(epsilon=epsilon, index_mapper=index_mapper) # This also calls reset() to reset sketch size
        if epsilon is not None:
            self.prob = 1 / (1 + math.pow(math.e, self.epsilon))
            self.c = (math.pow(math.e, epsilon) + 1) / (math.pow(math.e, epsilon) - 1)

    def _add_to_aggregate(self, data):
        v = data[0]
        o = data[1]
        k_sample = data[2]
        m_sample = data[3]

        all_value = np.where(self.hash_index[k_sample] == m_sample)[0]
        agg = [o[i][self.hash_index[i]] for i in self.n_hash]
        agg = np.reshape(agg, (self.k, self.estimation_num))
        minIndex = np.argmin(agg[:, all_value], axis=0)
        value = all_value[np.where(minIndex == k_sample)[0]]
        self.aggregated_data[value] = self.aggregated_data[value] + (v * (self.c / 2) + 0.5 * self.ones[value])

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
        self._add_to_aggregate(data)
        self.n += 1

    def estimate(self, data, suppress_warnings=False):
        self.check_warnings(suppress_warnings)
        self.check_and_update_estimates()
        return self.aggregated_data[data] * self.m * self.k


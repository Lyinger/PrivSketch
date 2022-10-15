import numpy as np
from frequency_oracles.privsketch import PrivSketchClient, PrivSketchServer

# Using PrivSketch

epsilon = 3 # Privacy budget of 3
k = 4
m = 8
d = 50

server = PrivSketchServer(epsilon=epsilon, k=k, m=m, estimation_items_num=d, d=d)
try:
    hash_funcs = server.get_hash_funcs()
except AttributeError:
    pass

client = PrivSketchClient(epsilon=epsilon, hash_funcs=hash_funcs, m=m, d=d)

data = list(np.array([1,2]*3000).reshape(3000, 2)) + list(np.array([1,3]*2000).reshape(2000, 2)) + list(np.array([1,2,3]*2000).reshape(2000, 3)) + list(np.array([4]*2000).reshape(2000, 1)) + list(np.array([i for i in range(5, 51)]*1000).reshape(1000, 46))

for item in data:
    server.aggregate(client.privatise(item))

print(server.estimate(1))
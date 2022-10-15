import numpy as np
from core.fo_creator import *
import time

class PureSimulation():
    def __init__(self, name, client_params, server_params):
        super().__init__()
        self.client_params = client_params
        self.server_params = server_params
        self.normalization = server_params.get("normalization", 0)
        self.non_neg = True
        if self.normalization == "None":
            self.normalization = 0
            self.non_neg = False
        self.memory_safe = server_params.get("memory_safe", False)
        self.name = name

    def run(self, data, domain):
        d = len(domain)

        # -------------------- Simulating the client-side process --------------------
        ldp_data = []

        min_domain_val = min(domain)

        # Maps a data value x to {0, 1, ... , len(domain)-1} for indexing purposes
        if min_domain_val < 0:
            index_mapper = lambda x: x + abs(min_domain_val)
        else:
            index_mapper = lambda x: x - abs(min_domain_val)

        self.client_params["index_mapper"] = index_mapper
        self.server_params["index_mapper"] = index_mapper

        # Sometimes we want to override d values for experiments
        if self.client_params.get("d") is None and self.server_params.get("d") is None:
            self.client_params["d"] = d
            self.server_params["d"] = d

        if self.server_params.get("estimation_items_num") is None:
            self.server_params["estimation_items_num"] = d
        elif self.server_params["estimation_items_num"] > d:
            self.server_params["estimation_items_num"] = d

        start_time = time.time()
        server = create_fo_server_instance(self.name, self.server_params)
        server_init_time = time.time() - start_time

        # Some clients need hash functions as parameters
        try:
            hash_funcs = server.get_hash_funcs()
            self.client_params["hash_funcs"] = hash_funcs
        except AttributeError:
            pass

        try:
            server_fo_hash_funcs = server.server_fo_hash_funcs
            self.client_params["server_fo_hash_funcs"] = server_fo_hash_funcs
        except AttributeError:
            pass

        start_time = time.time()
        client = create_fo_client_instance(self.name, self.client_params)
        # using data here

        if not self.memory_safe:
            for i in range(0, len(data)):
                ldp_data.append(client.privatise(data[i]))

            client_time = time.time() - start_time

            # -------------------- Simulating the server-side process --------------------

            # Simulate aggregation
            start_time = time.time()
            for index, item in enumerate(ldp_data):
                server.aggregate(item)

            agg_time = (time.time() - start_time)
        else:
            last_server_time = start_time
            client_time = 0
            agg_time = 0
            for i in range(0, len(data)):
                perturbed_data = client.privatise(data[i])
                last_client_time = time.time()
                client_time += last_client_time - last_server_time

                server.aggregate(perturbed_data)
                last_server_time = time.time()
                agg_time += last_server_time - last_client_time

        start_time = time.time()
        ldp_freq = server.estimate_all(np.arange(self.server_params["estimation_items_num"]), normalization=self.normalization)
        est_time = time.time() - start_time

        server_time = server_init_time + agg_time + est_time
        ldp_plot_data = list(map(lambda x: int(round(x)), ldp_freq))

        results = {}
        results["plot_data"] = ldp_plot_data
        results["client_time"] = client_time
        results["server_time"] = server_time
        results["server_agg_time"] = agg_time
        results["server_est_time"] = est_time
        results['server_init_time'] = server_init_time

        return results

import random
from simulations.helpers.FrequencyOracleSimulation import FrequencyOracleSimulation
import copy
import numpy as np


# #-------------------- Parameters for simulation --------------------

# --------- General Parameters -----------
N = 100000
epsilon = 3
k = 4
m = 128

# ------------ CMS ------------
cms_params = {"m": m, "k": k, "epsilon": epsilon}
cms = {"client_params": cms_params, "server_params": cms_params}

def loadData(filePath):
    f = open(filePath, "r")
    dataList = []
    totalData = []
    line = f.readline()
    while line:
        d = list(map(int, line.strip().split(" ")))
        dataList.append(d)
        totalData += d
        line = f.readline()
    return dataList, totalData

def loadPaddingSamplingData(filePath):
    f = open(filePath, "r")
    dataList = []
    totalData = []
    line = f.readline()
    dlen = 78
    while line:
        d = list(map(int, line.strip().split(" ")))
        if len(d) >= dlen:
            dataList.append(random.sample(d,dlen))
        else:
            dataList.append(d)
        totalData += d
        line = f.readline()
    return dataList, totalData

# Multi-PCMS-Mean
def multiPCMSMean_vary_eps(dataList, totalData):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    k = 4
    m = 128

    repeats = 10
    epsilons = np.arange(1, 11, 1)

    experiment_list = []
    for i in range(0, repeats):
        for e in epsilons:
            mean_sketch = copy.deepcopy(cms)

            mean_sketch["server_params"]["m"] = m
            mean_sketch["client_params"]["m"] = m
            mean_sketch["server_params"]["k"] = k
            mean_sketch["client_params"]["k"] = k
            mean_sketch["client_params"]["epsilon"] = e
            mean_sketch["server_params"]["epsilon"] = e
            mean_sketch["server_params"]["memory_safe"] = True

            mean_sketch["data"] = dataList
            mean_sketch["multiple_data"] = dict()
            mean_sketch["multiple_data"]["times"] = 1
            mean_sketch["multiple_data"]["combined"] = totalData

            experiment_list.append((("MultiPCMSMean", "e=" + str(e)), mean_sketch))

    simulation.run_and_plot(experiment_list, display_stats_only=True)

# nPCMS
def  nPCMS_vary_eps(dataList, totalData):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    k = 4
    m = 128

    repeats = 10
    epsilons = np.arange(1, 11, 1)

    experiment_list = []
    for i in range(0, repeats):
        for e in epsilons:
            mean_sketch = copy.deepcopy(cms)

            mean_sketch["server_params"]["m"] = m
            mean_sketch["client_params"]["m"] = m
            mean_sketch["server_params"]["k"] = k
            mean_sketch["client_params"]["k"] = k
            mean_sketch["client_params"]["epsilon"] = e
            mean_sketch["server_params"]["epsilon"] = e
            mean_sketch["server_params"]["memory_safe"] = True

            mean_sketch["data"] = dataList
            mean_sketch["multiple_data"] = dict()
            mean_sketch["multiple_data"]["times"] = 1
            mean_sketch["multiple_data"]["combined"] = totalData

            experiment_list.append((("nPCMS", "e=" + str(e)), mean_sketch))

    simulation.run_and_plot(experiment_list, display_stats_only=True)

# Multi-PCMS-Min
def multiPCMSMin_vary_eps(dataList, totalData):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    k = 4
    m = 128

    repeats = 10
    epsilons = np.arange(1, 11, 1)

    experiment_list = []
    for i in range(0, repeats):
        for e in epsilons:
            min_sketch = copy.deepcopy(cms)
            min_sketch["server_params"]["m"] = m
            min_sketch["client_params"]["m"] = m
            min_sketch["server_params"]["k"] = k
            min_sketch["client_params"]["k"] = k
            min_sketch["client_params"]["epsilon"] = e
            min_sketch["server_params"]["epsilon"] = e
            min_sketch["server_params"]["memory_safe"] = True

            min_sketch["data"] = dataList
            min_sketch["multiple_data"] = dict()
            min_sketch["multiple_data"]["times"] = 1
            min_sketch["multiple_data"]["combined"] = totalData

            experiment_list.append((("MultiPCMSMin", "e=" + str(e)), min_sketch))

    simulation.run_and_plot(experiment_list, display_stats_only=True)

# PrivSketch-noSmp
def PrivSketchPre_vary_eps(dataList, totalData):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    k = 4
    m = 128

    repeats = 10
    epsilons = np.arange(1, 11, 1)

    experiment_list = []
    for i in range(0, repeats):
        for e in epsilons:
            cms_params = copy.deepcopy(cms)
            freq_oracles = [cms_params]

            for fo in freq_oracles:
                fo["server_params"]["m"] = m
                fo["client_params"]["m"] = m
                fo["server_params"]["k"] = k
                fo["client_params"]["k"] = k
                fo["client_params"]["epsilon"] = e
                fo["server_params"]["epsilon"] = e
                fo["server_params"]["memory_safe"] = True

                fo["data"] = dataList
                fo["multiple_data"] = dict()
                fo["multiple_data"]["times"] = 1
                fo["multiple_data"]["combined"] = totalData

            experiment_list.append((("PrivSketchPre", "e=" + str(e)), cms_params))

    simulation.run_and_plot(experiment_list, display_stats_only=True)

# PrivSketch
def PrivSketch_vary_eps(dataList, totalData):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    k = 4
    m = 128

    repeats = 10
    epsilons = np.arange(1, 11, 1)

    experiment_list = []
    for i in range(0, repeats):
        for e in epsilons:
            cms_params = copy.deepcopy(cms)
            freq_oracles = [cms_params]

            for fo in freq_oracles:
                fo["server_params"]["m"] = m
                fo["client_params"]["m"] = m
                fo["server_params"]["k"] = k
                fo["client_params"]["k"] = k
                fo["client_params"]["epsilon"] = e
                fo["server_params"]["epsilon"] = e
                fo["server_params"]["memory_safe"] = True

                fo["data"] = dataList
                fo["multiple_data"] = dict()
                fo["multiple_data"]["times"] = 1
                fo["multiple_data"]["combined"] = totalData

            experiment_list.append((("PrivSketch", "e=" + str(e)), cms_params))

    simulation.run_and_plot(experiment_list, display_stats_only=True)

def sketch_vary_k(m, dataList, totalData):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    k_list = [2, 4, 8, 16, 32, 64, 128, 256]

    repeats = 10
    epsilons = [3]

    experiment_list = []
    sketch_est_types = ["MultiPCMSMean", "MultiPCMSMin", "PrivSketchPre", "PrivSketch"]
    for i in range(0, repeats):
        for e in epsilons:
            for k in k_list:
                for j, sketch_est_type in enumerate(sketch_est_types):
                    cms_params = copy.deepcopy(cms)
                    cms_params["server_params"]["m"] = m
                    cms_params["client_params"]["m"] = m
                    cms_params["server_params"]["k"] = k
                    cms_params["client_params"]["k"] = k
                    cms_params["client_params"]["epsilon"] = e
                    cms_params["server_params"]["epsilon"] = e
                    cms_params["server_params"]["memory_safe"] = True

                    cms_params["data"] = dataList
                    cms_params["multiple_data"] = dict()
                    cms_params["multiple_data"]["times"] = 1
                    cms_params["multiple_data"]["combined"] = totalData

                    experiment_list.append(((sketch_est_type, "k=" + str(k)), cms_params))
    simulation.run_and_plot(experiment_list, display_stats_only=True)

def sketch_vary_m(k, dataList, totalData):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    m_list = [4, 8, 16, 32, 64, 128, 256, 512, 1024]

    repeats = 10
    epsilons = [3]

    experiment_list = []
    sketch_est_types = ["MultiPCMSMean", "MultiPCMSMin", "PrivSketchPre", "PrivSketch"]
    for i in range(0, repeats):
        for e in epsilons:
            for m in m_list:
                for j, sketch_est_type in enumerate(sketch_est_types):
                    cms_params = copy.deepcopy(cms)
                    cms_params["server_params"]["m"] = m
                    cms_params["client_params"]["m"] = m
                    cms_params["server_params"]["k"] = k
                    cms_params["client_params"]["k"] = k
                    cms_params["client_params"]["epsilon"] = e
                    cms_params["server_params"]["epsilon"] = e
                    cms_params["server_params"]["memory_safe"] = True

                    cms_params["data"] = dataList
                    cms_params["multiple_data"] = dict()
                    cms_params["multiple_data"]["times"] = 1
                    cms_params["multiple_data"]["combined"] = totalData

                    experiment_list.append(((sketch_est_type, "m=" + str(m)), cms_params))
    simulation.run_and_plot(experiment_list, display_stats_only=True)

def sketch_vary_d(dataPath):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    k = 4
    m = 128

    repeats = 10
    epsilons = [3]

    d_list = [20000, 40000, 60000, 80000, 100000]
    experiment_list = []
    sketch_est_types = ["MultiPCMSMean", "MultiPCMSMin", "PrivSketchPre", "PrivSketch"]

    for d in d_list:
        data_list, total = loadData(dataPath + "\\0_synthetic_l10_d" + str(d) + "_n10000_s1-1.csv")
        for i in range(0, repeats):
            for e in epsilons:
                for j, sketch_est_type in enumerate(sketch_est_types):
                    cms_params = copy.deepcopy(cms)
                    cms_params["server_params"]["m"] = m
                    cms_params["client_params"]["m"] = m
                    cms_params["server_params"]["k"] = k
                    cms_params["client_params"]["k"] = k
                    cms_params["client_params"]["epsilon"] = e
                    cms_params["server_params"]["epsilon"] = e
                    cms_params["server_params"]["memory_safe"] = True

                    cms_params["data"] = data_list
                    cms_params["multiple_data"] = dict()
                    cms_params["multiple_data"]["times"] = 1
                    cms_params["multiple_data"]["combined"] = total
                    experiment_list.append(((sketch_est_type, "d=" + str(d)), cms_params))
    simulation.run_and_plot(experiment_list, display_stats_only=True)

def sketch_times_vary_items(dataLen, dataPath, filename):
    top_k = 50
    simulation = FrequencyOracleSimulation([0], "", display_full_stats=True, calc_top_k=top_k, autosave=True)
    k = 4
    m = 128

    repeats = 1
    epsilons = [3]

    item_list = [int(dataLen*0.0001), int(dataLen*0.001), int(dataLen*0.01), int(dataLen*0.1), dataLen]
    experiment_list = []
    sketch_est_types = ["MultiPCMSMean", "MultiPCMSMin", "PrivSketchPre", "PrivSketch"]

    for item in item_list:
        data_list, total = loadData(dataPath + filename)
        for i in range(0, repeats):
            for e in epsilons:
                for j, sketch_est_type in enumerate(sketch_est_types):
                    cms_params = copy.deepcopy(cms)
                    cms_params["server_params"]["m"] = m
                    cms_params["client_params"]["m"] = m
                    cms_params["server_params"]["k"] = k
                    cms_params["client_params"]["k"] = k
                    cms_params["client_params"]["epsilon"] = e
                    cms_params["server_params"]["epsilon"] = e
                    cms_params["server_params"]["memory_safe"] = True
                    cms_params["server_params"]["estimation_items_num"] = item

                    cms_params["data"] = data_list
                    cms_params["multiple_data"] = dict()
                    cms_params["multiple_data"]["times"] = 1
                    cms_params["multiple_data"]["combined"] = total

                    experiment_list.append(((sketch_est_type, "items=" + str(item)), cms_params))
    simulation.run_and_plot(experiment_list, display_stats_only=True)


dataPath = "../dataset/"
filename = "1_synthetic_l100_d100000_n100000_s1-1.csv"

# different eps on Dataset1
data, total = loadPaddingSamplingData(dataPath + filename)
nPCMS_vary_eps(data, total)

data, total = loadData(dataPath + filename)
multiPCMSMean_vary_eps(data, total)
multiPCMSMin_vary_eps(data, total)
PrivSketchPre_vary_eps(data, total)
PrivSketch_vary_eps(data, total)

# different m with fixed k for all protocols
sketch_vary_m(4, data, total) # set fixed k

# different k with fixed m for all protocols
sketch_vary_k(32, data, total) # set fixed m

# different numbers of estimated items for all protocols
sketch_times_vary_items(len(np.unique(total)), dataPath, filename)
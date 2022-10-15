
import numpy as np
from collections import Counter


def generate_len_data(l=100, n=1000000):
    lenArr = (np.random.normal(1, 0.2, n) * l).astype(int)
    lenArr = lenArr - np.min(lenArr) + 1
    totalLen = np.sum(lenArr)
    print(totalLen)
    print(np.min(lenArr))
    print(np.max(lenArr))
    return lenArr, totalLen

def generate_zipf_data(d, totalLen, large_domain=False, s=1.1):
    data = np.random.zipf(s, totalLen).astype(int)  # Generate test data
    data_counter = Counter(data)
    keys, freqs = zip(*data_counter.most_common(d))
    key_dict = dict(zip(keys, range(0, len(keys))))

    if large_domain:
        d1 = [key_dict[item] for item in keys]  # identifier
        d2 = data[np.where(np.in1d(data, keys))]  # top-d data
        d2 = [key_dict[item] for item in d2]  # top-d data identifier
        d2 = np.random.choice(d2, size=totalLen - len(d1))
        data = np.concatenate([d1, d2])
    else:
        data = data[np.where(np.in1d(data, keys))]
        data = [key_dict[item] for item in data]
        data = np.random.choice(data, size=totalLen)

    print("Total Size of Dataset:", len(data))
    print("Total unique items:", len(Counter(data).keys()))
    print("Max Frequency: ", max(Counter(data).values()))
    return data

def generate_synthetic_data(dstPath):
    l = 10
    d = 100000
    n = 100000
    s = 1.1
    lenArr, totalLen = generate_len_data(l,n)
    data = np.random.permutation(generate_zipf_data(d, totalLen, large_domain=True, s=s))

    dst = open(dstPath + "/synthetic_l"+str(l)+"_d"+str(d)+"_n"+str(n)+"_s"+str(s).replace(".","-")+".csv", "w")
    lenIndex = 0
    for len in lenArr:
        user_data = []
        for j in range(len):
            user_data.append(data[lenIndex+j])
        dst.write(str(list(np.unique(user_data)))[1:-1].replace(" ", "").replace(",", " ")+"\n")
        lenIndex += len

generate_synthetic_data("./dataset")

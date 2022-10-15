# PrivSketch

## Protocols Execution

In `example.py`, we present a running example for PrivSketch. You can run it directly:
```shell
cd ./PrivSketch
python ./example.py
```
You can change the data to your own datasets or try to execute other protocols implemented here:
* nPCMS: an extension for Private Count-Mean Sketch (PCMS-Mean, Apple) by running multiple times, implemented in `frequency_oracles.pcms`
* Multi-PCMS-Mean: an extension for PCMS-Mean by encoding multiple items in one sketch, implemented in `frequency_oracles.pcms`
* Multi-PCMS-Min: a variant of Multi-PCMS-Mean by substituting the mean-estimation with the min-estimation, implemented in `frequency_oracles.pcms`
* PrivSketch-noSmp: a pre-version of PrivSketch which does not implement the sampling, implemented in `frequency_oracles.privsketch`

## Experiments
There are some dataset examples under the path `./dataset`.

### Synthetic Datasets Generation
To generate a synthetic data following the Zipf distribution, 

```shell
cd ./PrivSketch
python ./simulations/data_generator.py
```
The generated synthetic dataset is saved under the path `./dataset` in a `csv` file. It has a default setting with domain `d = 100,000`, the number of users
`n = 100, 000` and the number of items each user has is following a normal distribution with an expectation of `100`. You can change these parameter settings in the function *generate_synthetic_data*.

### Experiment Conduction

As shown in `./simulation/experiments.py`, to conduct experiments on these protocols, you should set the path and name of the dataset, and load it:
```python
dataPath = "../dataset/"
filename = "1_synthetic_l100_d100000_n100000_s1-1.csv"
data, total = loadData(dataPath + filename)
```
Since the nPCMS protocol needs to implement the *padding and sampling* technique, its loading process is slightly different:
```python
data, total = loadPaddingSamplingData(dataPath + filename)
```
There is a basic example for experiments under different epsilon.
```python
nPCMS_vary_eps(data, total)
multiPCMSMean_vary_eps(data, total)
multiPCMSMin_vary_eps(data, total)
PrivSketchPre_vary_eps(data, total)
PrivSketch_vary_eps(data, total)
```
See `./simulations/experiments.py` for more experiments.

## Acknowledgements
The PCMS related code is based on the implementation [Samuel Maddock/pure-LDP](https://github.com/Samuel-Maddock/pure-LDP).
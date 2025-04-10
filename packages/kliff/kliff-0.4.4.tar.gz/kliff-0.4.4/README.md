# KIM-based Learning-Integrated Fitting Framework (KLIFF)

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/openkim/kliff/testing.yml)
[![Documentation Status](https://readthedocs.org/projects/kliff/badge/?version=latest)](https://kliff.readthedocs.io/en/latest/?badge=latest)
[![Anaconda-Server Badge](https://img.shields.io/conda/vn/conda-forge/kliff.svg)](https://anaconda.org/conda-forge/kliff)
[![PyPI](https://img.shields.io/pypi/v/kliff.svg)](https://pypi.python.org/pypi/kliff)

### Documentation at: <https://kliff.readthedocs.io>

KLIFF is an interatomic potential fitting package that can be used to fit physics-motivated (PM) potentials, as well as machine learning potentials such as the neural network (NN) models.

## Installation

### Using conda (recommended)

```sh
conda install -c conda-forge kliff
```

### Using pip

```sh
pip install kliff
```

### From source

```
git clone https://github.com/openkim/kliff
pip install ./kliff
```

### Dependencies

- KLIFF requires the [kim-api](https://openkim.org/kim-api/) and [kimpy](https://github.com/openkim/kimpy) packages.
  If you install using `conda` as described above, these packages will be installed automatically. Alternatively, they can be installed from source or via [pip](https://pip.pypa.io/en/stable/).
  See [Installation](https://kliff.readthedocs.io/en/latest/installation.html) for more information.

- In addition, [PyTorch](https://pytorch.org) is needed if you want to train machine learning models. See the official [PyTorch website](https://pytorch.org/get-started/locally/) for installation instructions.

## A quick example to train a neural network potential

```python
from kliff import nn
from kliff.calculators import CalculatorTorch
from kliff.descriptors import SymmetryFunction
from kliff.dataset import Dataset
from kliff.models import NeuralNetwork
from kliff.loss import Loss
from kliff.utils import download_dataset

# Descriptor to featurize atomic configurations
descriptor = SymmetryFunction(
    cut_name="cos", cut_dists={"Si-Si": 5.0}, hyperparams="set51", normalize=True
)

# Fully-connected neural network model with 2 hidden layers, each with 10 units
N1 = 10
N2 = 10
model = NeuralNetwork(descriptor)
model.add_layers(
    # first hidden layer
    nn.Linear(descriptor.get_size(), N1),
    nn.Tanh(),
    # second hidden layer
    nn.Linear(N1, N2),
    nn.Tanh(),
    # output layer
    nn.Linear(N2, 1),
)

# Training set (dataset will be downloaded from:
# https://github.com/openkim/kliff/blob/master/examples/Si_training_set.tar.gz)
dataset_path = download_dataset(dataset_name="Si_training_set")
dataset_path = dataset_path.joinpath("varying_alat")
train_set = Dataset(dataset_path)
configs = train_set.get_configs()

# Set up calculator to compute energy and forces for atomic configurations in the
# training set using the neural network model
calc = CalculatorTorch(model, gpu=False)
calc.create(configs)

# Define a loss function and train the model by minimizing the loss
loss = Loss(calc)
result = loss.minimize(method="Adam", num_epochs=10, batch_size=100, lr=0.001)

# Write trained model as a KIM model to be used in other codes such as LAMMPS and ASE
model.write_kim_model()
```

Detailed explanation and more tutorial examples can be found in the [documentation](https://kliff.readthedocs.io/en/latest/tutorials.html).

## Why you want to use KLIFF (or not use it)

- Interacting seamlessly with[ KIM](https://openkim.org), the fitted model can be readily used in simulation codes such as LAMMPS and ASE via the `KIM API`
- Creating mixed PM and NN models
- High level API, fitting with a few lines of codes
- Low level API for creating complex NN models
- Parallel execution
- [PyTorch](https://pytorch.org) backend for NN (include GPU training)

## Citing KLIFF

```
@Article{wen2022kliff,
  title   = {{KLIFF}: A framework to develop physics-based and machine learning interatomic potentials},
  author  = {Mingjian Wen and Yaser Afshar and Ryan S. Elliott and Ellad B. Tadmor},
  journal = {Computer Physics Communications},
  volume  = {272},
  pages   = {108218},
  year    = {2022},
  doi     = {10.1016/j.cpc.2021.108218},
}
```

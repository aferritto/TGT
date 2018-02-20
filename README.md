# TGT: TGT Generates Terrain
### Terrain Generation via Machine Learning

[![Build Status](https://travis-ci.org/ferria/TGT.svg?branch=master)](https://travis-ci.org/ferria/TGT)
[![Coverage Status](https://coveralls.io/repos/github/ferria/TGT/badge.svg?branch=master)](https://coveralls.io/github/ferria/TGT?branch=master)

TGT is being developed to leverage machine learning techniques to assist in terrain generation.  Our eventual goal is to be able to effectively generate terrain and integrate our functionality with [Soul Engine](https://github.com/Synodic-Software/Soul-Engine).

Stay tuned for issues as they become available for opportunities to contribute.


## Installing and Updating the Conda Env

To install the conda environment for this project you can run ```conda env create -f environment.yml```.

To update an existing environment for this project you can run ```conda env update --prune -f environment.yml```.

Activate the environment using:
- ```activate tgt``` (Windows)
- ```source activate tgt``` (macOS and Linux)

More information can be found in the conda 
[docs](https://conda.io/docs/user-guide/tasks/manage-environments.html).


## Running the Tests

The project tests can be run by calling ```python -m pytest --cov=tgt tests/``` 
in the top level directory of the project.  This also checks coverage.

The following can be used to check pep8 compliance:
- ```pycodestyle --show-source tgt/```
- ```pycodestyle --show-source tests/```

For a full list of commands used to build and test the project please see ```.travis.yml``` and 
```build/build_environment.sh```.
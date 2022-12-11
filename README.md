# Finance Follower

---

# Setting the ambient

___

## Install conda

Get anaconda installer on <https://www.anaconda.com/products/distribution>

Download and install the latest version of conda.

___

## Creating environment for the project

This file contains all necessary package for the project.

```
conda env create -f ff.yml
```
___

## Linter

Install any linter for the project.

 * [Pycharm](https://github.com/leinardi/pylint-pycharm)
 * [VSCode](https://code.visualstudio.com/docs/python/linting)

___

#Coding standards

###**This project uses the PEP8 style guide convention.**
For any doubts, please refer to the official [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/).

___

## Naming types

* b (single lowercase letter)

* B (single uppercase letter)

* lowercase

* lower_case_with_underscores

* UPPERCASE

* UPPER_CASE_WITH_UNDERSCORES

* CapitalizedWords (or CapWords, or CamelCase – so named because of the bumpy look of its letters [4]).

* mixedCase (differs from CapitalizedWords by initial lowercase character!)
Capitalized_Words_With_Underscores


## Naming guide

* **Packages and Module Names** - lowercase


* **Class Names** - CamelCase


* **Global Variable Names** - lower_case_with_underscores


* **Function and Variable Names** - lower_case_with_underscores


* **Constants** - UPPER_CASE_WITH_UNDERSCORES


* **Attribute** - lower_case_with_underscores


___

#Usefull commands:

##  Exporting the environment

* Linux:
```
conda env export --no-builds | grep -v "prefix" > ff.yml
```

* Windows:
```
conda env export --no-builds | findstr -v "prefix" > ff.yml
```

##  Deleting and Creating the environment

```
conda deactivate 
conda remove -n FinanceFollower --all
conda env create --file ff.yml
conda activate FinanceFollower
```
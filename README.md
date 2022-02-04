
# Add normweight branch to dijet TTrees

The normweight branch is constructed as follow:

<div align=center>mcEventWeight * cross-section * efficiency * kFactor / sum of weights</div>

## 1. Merge all ROOT files from a given DSID and add the normweight branch

### How to use it?

#### 1. Setup

```source Setup.sh```

#### 2. Use ```MergeTTrees.py``` script to merge dijet ntuples.

**Syntax:**

```
python MergeTTrees.py --inDir [INPUT_DIRECTORY] --outDir [OUTPUT_DIRECTORY]
```

**Optional flags:**

- ```--debug```: enables debug logging
- ```--dryRun```: doesn't merge anything

**Please note:** ```INPUT_DIRECTORY``` must contain the dataset name of the grid job (in order to extract information)

## 2. Take each individual ROOT file, add normweight branch and create a new '_expanded.root' file

### How to use it?

#### 1. Setup

```source Setup.sh```

#### 2. Use ```add_normweights.py``` script.

**Syntax:**

```
python add_normweights.py --inDir [INPUT_DIRECTORY] --outDir [OUTPUT_DIRECTORY]
```

**Optional flags:**

- ```--debug```: enables debug logging
- ```--dryRun```: doesn't create output ROOT files

**Please note:** ```INPUT_DIRECTORY``` must contain the dataset name of the grid job (in order to extract information)

An example submission script to run over all slices is provided: 'run_add_normweights.py'



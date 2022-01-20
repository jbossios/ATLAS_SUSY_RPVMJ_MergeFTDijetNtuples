
# How to use it?

1. Setup: ```source Setup.sh```

2. Use ```MergeTTrees.py``` script to merge dijet ntuples.

<u>Syntax</u>

python MergeTTrees.py --inDir [INPUT_DIRECTORY] --outDir [OUTPUT_DIRECTORY]

Optional flags:

- --debug: enables debug logging
- --dryRun: doesn't merge anything

**Please note:** ```INPUT_DIRECTORY``` must contain the dataset name of the grid job (in order to extract information)

# HUI-Audio-Corpus-German
This is the official repository for the HUI-Audio-Corpus-German. The corresponding paper is in the process of publication.  With the repository it is possible to automatically recreate the dataset. It is also possible to add more speakers to the processing pipeline.


## Speaker overview

* bernd
* hokuspokus
* friedrich
* eva
* karlsson
* sonja

### Not finisched

* redaer

## Installation

### Requirements

* Linux
* Anaconda 

### Setup python environment with Anaconda

Navigate with the terminal to the colned repository

Create a new conda environment (For more informations: https://salishsea-meopar-docs.readthedocs.io/en/latest/work_env/python3_conda_environment.html)
```
conda create -n huiAudioCorpus python=3.8
conda activate huiAudioCorpus
```

Install the package as devolop python package (For more informations: http://naoko.github.io/your-project-install-pip-setup/)

```
python setup.py develop
```

Install dependencys
```
pip install -r requirements.txt 
```

Download: ***************** and copy the content of the downloaded zip into the folder:

```
/huiAudioCorpus/sttInference/deepspeechModel
```
### Optional installation step
The deepspeech model runs by default on CPU. This could lead to a long pipeline processing pipeline. If you have a compatible GPU you can install a special version from deepspeech.
More infos can be found at:
```
https://deepspeech.readthedocs.io/en/r0.9/USING.html
```
## Recreate dataset

To execute the script you can use the crate Script
```
cd scripts

python createDataset.py
```

Here you are able to take a view configurations:

Inside the variable "allConfigs" you can add all speacker configurations. If you want to test fast if the pipeline is runnig you can use:

```
allConfigs = sonja
```

for all speackers you could use

```
allConfigs = {**bernd, **hokuspokus, **friedrich, **eva, **karlsson, **sonja}
```

The processing files and the complete dataset with statistics are createt at the folder
```
/datasetWorkflow
```
you can change the directory inside teh createDataset.py

```
externalPaths = [
    "/path/to/the/folder"
]

```

## Create new speacker

If you want to 

## Create statistic for other datasets


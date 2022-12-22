# HUI-Audio-Corpus-German
This is the official repository for the HUI-Audio-Corpus-German. The corresponding paper is in the process of publication.  With this repository it is possible to automatically recreate the dataset. It is also possible to add more speakers to the processing pipeline.

Dataset: https://opendata.iisys.de/datasets.html

Live example: http://narvi.sysint.iisys.de/projects/tts

Paper(under review): https://arxiv.org/abs/2106.06309

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

Navigate to the cloned repository

Create a new conda environment (For more informations: https://salishsea-meopar-docs.readthedocs.io/en/latest/work_env/python3_conda_environment.html)
```
conda create -n huiAudioCorpus python=3.8
conda activate huiAudioCorpus
```

Install the package as devolop python package (For more informations: http://naoko.github.io/your-project-install-pip-setup/)

```
python setup.py develop
```

Installation of dependencies
```
pip install -r requirements.txt 
```

Download: https://opendata.iisys.de/opendata/Datasets/deepspeechModel/deepspeechModel.zip and copy the content of the downloaded zip into the folder:

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

```
cd scripts

python createDataset.py
```

Here, configurations can be viewed:

Inside the variable "allConfigs" all speaker configurations can be added. If you want to easily test if the pipeline is runnig you can use:

```
allConfigs = sonja
```

for all speakers you could use

```
allConfigs = {**bernd, **hokuspokus, **friedrich, **eva, **karlsson, **sonja}
```

The processing files and the complete dataset with statistics are created at
```
/datasetWorkflow
```
Directory can be changed inside createDataset.py

```
externalPaths = [
    "/path/to/the/folder"
]

```

## Adding a new speaker

If you want to add a new speaker, follow these steps:
* Create a json file inside the scripts/createDatasetConfig with your speaker. Here you can find examples of how the file should look. Infos about the speacers can be found at datasetWorkflow/overview
* Validate text replacements, the script helps you with the needed steps
* finish dataset and create a push request

## Creating statistics for other datasets

We have a script for the creation of statistics only.
For this, variables "loadPath" and "savePath" inside the file "scripts/generrateAudioStatistic.py" have to be adjusted.

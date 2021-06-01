from typing import Dict
from ttsCode.src.dependencyInjection.DependencyInjection import DependencyInjection
import datasetWorkflow
import ttsCode.scripts.createDatasetConfig as createDatasetConfig
from ttsCode.src.utils.PathUtil import PathUtil
import os

pathUtil = PathUtil()
basePath = createDatasetConfig.__path__[0]  # type: ignore

externalPaths = [
    'E:/repositorys/textToSpeech/datasetWorkflow',
    '/mnt/e/repositorys/textToSpeech/datasetWorkflow',
    '/media/ppuchtler/TOSHIBA_EXT/repositorys/textToSpeech/datasetWorkflow',
]

dataBasePath = datasetWorkflow.__path__[0]  # type: ignore
for path in externalPaths:
    if pathUtil.fileExists(path):
        dataBasePath = path

def logStep(name):
    print('')
    print('')
    print('#######################################################')
    print(name)
    print('#######################################################')
    print('')


bernd_1 = pathUtil.loadJson(
    basePath + '/Bernd_Ungerer_tausendUndEineNacht.json')
bernd_2 = pathUtil.loadJson(basePath + '/Bernd_Ungerer_other.json')
bernd = {**bernd_1, **bernd_2}
hokuspokus = pathUtil.loadJson(basePath + '/Hokuspokus.json')
redaer = pathUtil.loadJson(basePath + '/redaer.json')
friedrich = pathUtil.loadJson(basePath + '/Friedrich.json')
eva = pathUtil.loadJson(basePath + '/Eva.json')
karlsson = pathUtil.loadJson(basePath + '/Karlsson.json')
sonja = pathUtil.loadJson(basePath + '/Sonja.json')

allLibriboxIds = [author[key]['LibrivoxBookName'] for author in [
    bernd, hokuspokus, friedrich, eva, karlsson, redaer] for key in author]
duplicatIds = set([x for x in allLibriboxIds if allLibriboxIds.count(x) > 1])

if len(duplicatIds) > 0:
    raise Exception("Duplicate Librivox ids: " + str(duplicatIds))


allConfigs = {**bernd, **hokuspokus, **friedrich, **eva, **karlsson, **sonja}

#allConfigs = redaer

specialSpeackers = ['Bernd_Ungerer', 'Eva_K', 'Friedrich', 'Hokuspokus', 'Karlsson']

workflowConfig = {
    'continueOnError': False,
    'prepareAudio': False,
    'prepareText': False,
    'transcriptText': False,
    'alignText': False,
    'finalize': False,
    'audioRawStatistic': False,
    'cleanStatistic': True,
    'fullStatistic': True,
    'generateClean': False
}


step0Path = dataBasePath + '/overview'
logStep('Step0_Overview')
config = {
    'audiosFromLibrivoxPersistenz': {
        'bookName': '',
        'savePath': '',
        'chapterPath': ''
    },
    'step0_Overview': {
        'savePath': step0Path
    }
}
DependencyInjection(config).step0_Overview.run()

finalDatasetPath = dataBasePath + '/finalDataset'
finalDatasetPathClean = dataBasePath + '/finalDatasetClean'
step7Path = dataBasePath + '/rawStatistic'
setp8Path = dataBasePath + '/datasetStatistic'
setp8Path_clean = dataBasePath + '/datasetStatisticClean'


def cleanFilter(input):
    input = input[input['minSilenceDB'] < -50]
    input = input[input['silencePercent'] < 45]
    input = input[input['silencePercent'] > 10]
    return input

def runWorkflow(params: Dict, workflowConfig: Dict):
    print(params)
    bookBasePath = dataBasePath + '/books/'

    step1Path = bookBasePath + params['title'] + '/Step1_DownloadAudio'
    step1PathAudio = step1Path + '/audio'
    step1PathChapter = step1Path + '/chapter.csv'
    step2Path = bookBasePath + params['title'] + '/Step2_SplitAudio'
    step2_1_Path = bookBasePath + params['title'] + '/Step2_1_AudioStatistic'

    step2PathAudio = step2Path + '/audio'
    step3Path = bookBasePath + params['title'] + '/Step3_DownloadText'
    step3PathText = step3Path + '/text.txt'
    step3_1_Path = bookBasePath + params['title'] + '/Step3_1_PrepareText'
    step3_1_PathText = step3_1_Path + '/text.txt'

    step4Path = bookBasePath + params['title'] + '/Step4_TranscriptAudio'
    step5Path = bookBasePath + params['title'] + '/Step5_AlignText'
    step6Path = bookBasePath + params['title'] + '/Step6_FinalizeDataset'

    if workflowConfig['prepareAudio']:
        logStep('Step1_DowloadAudio')
        config = {
            'audiosFromLibrivoxPersistenz': {
                'bookName': params['LibrivoxBookName'],
                'savePath': step1PathAudio + '/',
                'chapterPath': step1PathChapter
            },
            'step1_DownloadAudio': {
                'savePath': step1Path
            }
        }
        DependencyInjection(config).step1_DownloadAudio.run()

        logStep('Step2_SplitAudio')
        config = {
            'audioSplitTransformer': {
                'minAudioDuration': 5,
                'maxAudioDuration': 40
            },
            'audioPersistenz': {
                'loadPath': step1PathAudio,
                'savePath': step2PathAudio,
                'fileExtension': 'mp3'
            },
            'audioLoudnessTransformer': {
                'loudness': -20
            },
            'step2_SplitAudio': {
                'bookName': params['title'],
                'savePath': step2Path,
                'remapSort': params['remapSort'] if 'remapSort' in params else None
            }
        }
        DependencyInjection(config).step2_SplitAudio.run()

        logStep('Step2_1_AudioStatistic')
        config = {
            'step2_1_AudioStatistic': {
                'savePath': step2_1_Path,
            },
            'audioPersistenz': {
                'loadPath': step2PathAudio
            },
            'plot': {
                'showDuration': 1,
                'savePath': step2_1_Path
            }
        }
        DependencyInjection(config).step2_1_AudioStatistic.run()

    if workflowConfig['prepareText']:
        logStep('Step3_DowloadText')
        config = {
            'GutenbergBookPersistenz': {
                'textId': params['GutenbergId'],
                'savePath': step3PathText
            },
            'step3_DowloadText': {
                'savePath': step3Path
            }
        }
        DependencyInjection(config).step3_DowloadText.run()

        logStep('Step3_1_PrepareText')
        config = {
            'step3_1_PrepareText': {
                'savePath': step3_1_Path,
                'loadFile': step3PathText,
                'saveFile': step3_1_PathText,
                'textReplacement': params['textReplacement'],
                'startSentence': params['GutenbergStart'],
                'endSentence': params['GutenbergEnd'],
                'moves': params['moves'] if 'moves' in params else [],
                'remove': params['remove'] if 'remove' in params else []
            }
        }
        DependencyInjection(config).step3_1_PrepareText.run()

    if workflowConfig['transcriptText']:
        logStep('Step4_TranscriptAudio')
        config = {
            'step4_TranscriptAudio': {
                'savePath': step4Path,
            },
            'audioPersistenz': {
                'loadPath': step2PathAudio
            },
            'transcriptsPersistenz': {
                'loadPath': step4Path,
            }
        }
        DependencyInjection(config).step4_TranscriptAudio.run()

    if workflowConfig['alignText']:
        logStep('Step5_AlignText')
        config = {
            'step5_AlignText': {
                'savePath': step5Path,
                'textToAlignPath': step3_1_PathText
            },
            'transcriptsPersistenz': {
                'loadPath': step4Path,
                'savePath': step5Path
            }
        }
        DependencyInjection(config).step5_AlignText.run()

    if workflowConfig['finalize']:
        logStep('Step6_FinalizeDataset')
        config = {
            'step6_FinalizeDataset': {
                'savePath': step6Path,
                'chapterPath': step1PathChapter
            },
            'audioPersistenz': {
                'loadPath': step2PathAudio,
                'savePath': finalDatasetPath
            },
            'transcriptsPersistenz': {
                'loadPath': step5Path,
                'savePath': finalDatasetPath
            }
        }
        DependencyInjection(config).step6_FinalizeDataset.run()


summary = {}
for configName in allConfigs:
    print('+++++++++++++++++++++++++++++++++++++++++')
    print('+++++++++++++++++++++++++++++++++++++++++')
    print('+++++++++++++++++++++++++++++++++++++++++')
    logStep(configName)
    print('+++++++++++++++++++++++++++++++++++++++++')
    print('+++++++++++++++++++++++++++++++++++++++++')
    print('+++++++++++++++++++++++++++++++++++++++++')

    config = allConfigs[configName]
    if workflowConfig['continueOnError']:
        try:
            runWorkflow(config, workflowConfig)
            summary[config['title']] = 'finished'
        except:
            summary[config['title']] = 'error'
    else:
        runWorkflow(config, workflowConfig)
print(summary)

if workflowConfig['audioRawStatistic']:
    logStep('audioRawStatistic')
    diConfig = {
        'step7_AudioRawStatistic': {
            'savePath': step7Path,
            'loadPath': finalDatasetPath
        }
    }
    DependencyInjection(diConfig).step7_AudioRawStatistic.run()

if workflowConfig['fullStatistic']:
    logStep('fullStatistic')
    diConfig = {
        'step8_DatasetStatistic': {
            'savePath': setp8Path,
            'loadPath': step7Path + '/overview.csv',
            'specialSpeackers': specialSpeackers,
            'filter': None
        },
        'audioPersistenz': {
            'loadPath':''
        },
        'transcriptsPersistenz': {
            'loadPath':''
        },
        'plot': {
            'showDuration': 0
        }
    }
    DependencyInjection(diConfig).step8_DatasetStatistic.run()

if workflowConfig['cleanStatistic']:
    logStep('cleanStatistic')
    diConfig = {
        'step8_DatasetStatistic': {
            'savePath': setp8Path_clean,
            'loadPath': step7Path + '/overview.csv',
            'specialSpeackers': specialSpeackers,
            'filter': cleanFilter
        },
        'audioPersistenz': {
            'loadPath':''
        },
        'transcriptsPersistenz': {
            'loadPath':''
        },
        'plot': {
            'showDuration': 0
        }
    }
    DependencyInjection(diConfig).step8_DatasetStatistic.run()

if workflowConfig['generateClean']:
    logStep('generateClean')
    diConfig = {
        'step9_GenerateCleanDataset': {
            'savePath': finalDatasetPath,
            'infoFile': step7Path +'/overview.csv',
            'filter': cleanFilter
        },
        'transcriptsPersistenz': {
            'loadPath': finalDatasetPath,
            'savePath': finalDatasetPathClean
        },
        'audioPersistenz': {
            'loadPath': finalDatasetPath,
            'savePath': finalDatasetPathClean
        },
    }
    DependencyInjection(diConfig).step9_GenerateCleanDataset.run()
from numpy import source
from huiAudioCorpus.dependencyInjection.DependencyInjection import DependencyInjection

loadPath = '/media/ppuchtler/LangsameSSD/Projekte/espnet/egs2/HUI_Tacotron/tts1/inferences'
savePath = '/media/ppuchtler/LangsameSSD/Projekte/espnet/egs2/HUI_Tacotron/tts1/hokuspokus_statistic'

diConfig = {
'step7_AudioRawStatistic': {
    'savePath': savePath + '/raw',
    'loadPath': loadPath
}
}
DependencyInjection(diConfig).step7_AudioRawStatistic.run()

diConfig = {
    'step8_DatasetStatistic': {
        'savePath': savePath + '/stats',
        'loadPath': savePath + '/raw/overview.csv',
        'specialSpeackers': [],
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
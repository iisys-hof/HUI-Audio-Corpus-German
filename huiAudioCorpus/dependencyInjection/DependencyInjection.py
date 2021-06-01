def disableLog():
    logging.getLogger('matplotlib').disabled = True
    logging.getLogger('matplotlib.font_manager').disabled = True
    logging.getLogger('matplotlib.colorbar').disabled = True
    logging.getLogger('numba.core.ssa').disabled = True
    logging.getLogger('numba.core.interpreter').disabled = True
    logging.getLogger('numba.core.byteflow').disabled = True
    logging.getLogger('numba.ssa').disabled = True
    logging.getLogger('numba.byteflow').disabled = True
    logging.getLogger('numba.interpreter').disabled = True
    logging.getLogger('paramiko.transport.sftp').disabled = True
    logging.getLogger('paramiko.transport').disabled = True
    logging.getLogger('h5py._conv').disabled = True
    logging.getLogger().setLevel(logging.WARNING)
    
from huiAudioCorpus.workflows.createDatasetWorkflow.Step8_DatasetStatistic import Step8_DatasetStatistic
from huiAudioCorpus.workflows.createDatasetWorkflow.Step9_GenerateCleanDataset import Step9_GenerateCleanDataset
from huiAudioCorpus.workflows.createDatasetWorkflow.Step7_AudioRawStatistic import Step7_AudioRawStatistic
from huiAudioCorpus.workflows.createDatasetWorkflow.Step3_1_PrepareText import Step3_1_PrepareText
from huiAudioCorpus.workflows.createDatasetWorkflow.Step0_Overview import Step0_Overview
from huiAudioCorpus.workflows.createDatasetWorkflow.Step2_1_AudioStatistic import Step2_1_AudioStatistic
from huiAudioCorpus.workflows.createDatasetWorkflow.Step6_FinalizeDataset import Step6_FinalizeDataset
from huiAudioCorpus.transformer.SentenceDistanceTransformer import SentenceDistanceTransformer
from huiAudioCorpus.calculator.AlignSentencesIntoTextCalculator import AlignSentencesIntoTextCalculator
from huiAudioCorpus.workflows.createDatasetWorkflow.Step5_AlignText import Step5_AlignText
from huiAudioCorpus.converter.AudioToSentenceConverter import AudioToSentenceConverter
from huiAudioCorpus.workflows.createDatasetWorkflow.Step4_TranscriptAudio import Step4_TranscriptAudio
from huiAudioCorpus.persistenz.GutenbergBookPersistenz import GutenbergBookPersistenz
from huiAudioCorpus.workflows.createDatasetWorkflow.Step3_DownloadText import Step3_DownloadText
from huiAudioCorpus.transformer.AudioSplitTransformer import AudioSplitTransformer
from huiAudioCorpus.transformer.AudioLoudnessTransformer import AudioLoudnessTransformer
from huiAudioCorpus.workflows.createDatasetWorkflow.Step2_SplitAudio import Step2_SplitAudio
from huiAudioCorpus.persistenz.AudiosFromLibrivoxPersistenz import AudiosFromLibrivoxPersistenz
from huiAudioCorpus.workflows.createDatasetWorkflow.Step1_DownloadAudio import Step1_DownloadAudio
from huiAudioCorpus.converter.StringToSentencesConverter import StringToSentencesConverter
from huiAudioCorpus.transformer.GlowTtsConfigTransformer import GlowTtsConfigTransformer
from frosch import hook
hook(theme = 'paraiso_dark')
import logging
disableLog()

from huiAudioCorpus.utils.SecureFTP import SecureFTP
from huiAudioCorpus.transformer.YamlConfigurationTransformer import ParallelWaveGanConfigTransformer
from huiAudioCorpus.persistenz.YamlPersistenz import YamlPersistenz
from huiAudioCorpus.error.DependencyInjectionError import DependencyInjectionError
from huiAudioCorpus.converter.ListToHistogramConverter import ListToHistogramConverter
from huiAudioCorpus.converter.ListToStatisticConverter import ListToStatisticConverter
from huiAudioCorpus.ui.Plot import Plot
from huiAudioCorpus.components.TextStatisticComponent import TextStatisticComponent
from huiAudioCorpus.components.AudioStatisticComponent import AudioStatisticComponent
from huiAudioCorpus.converter.AudioToPowerMelSpectrogramConverter import AudioToPowerMelSpectrogramConverter
from huiAudioCorpus.converter.AudioToParallelWaveGanSpectrogramConverter import AudioToParallelWaveGanMelSpectrogramConverter
from huiAudioCorpus.utils.PathUtil import PathUtil
from huiAudioCorpus.utils.FileListUtil import FileListUtil
from huiAudioCorpus.persistenz.SpeakerPersistenz import SpeakerPersistenz
from huiAudioCorpus.converter.TranscriptsToSentencesConverter import TranscriptsToSentencesConverter
from huiAudioCorpus.persistenz.AudioTranscriptPairPersistenz import AudioTranscriptPairPersistenz
from huiAudioCorpus.components.SentencesToAudioComponent import SentencesToAudioComponent
from huiAudioCorpus.calculator.AudioFromMelSpectrogramSpeackerCallculator import AudioFromMelSpectrogramSpeackerCallculator
from huiAudioCorpus.calculator.MelSpectrogramFromSymbolSentenceSpeakerCallculator import MelSpectrogramFromSymbolSentenceSpeakerCallculator
from huiAudioCorpus.converter.PhoneticSentenceToSymbolSentenceConverter import PhoneticSentenceToSymbolSentenceConverter
from huiAudioCorpus.converter.SentenceToPhoneticSentenceConverter import SentenceToPhoneticSentenceConverter
from huiAudioCorpus.transformer.AudioAddSilenceTransformer import AudioAddSilenceTransformer
from huiAudioCorpus.transformer.TranscriptsSelectionTransformer import TranscriptsSelectionTransformer
from huiAudioCorpus.workflows.ResampleCopyFilterAudioWorkflow import ResampleCopyFilterAudioWorkflow
from huiAudioCorpus.transformer.AudioSamplingRateTransformer import AudioSamplingRateTransformer
from huiAudioCorpus.persistenz.TranscriptsPersistenz import TranscriptsPersistenz
from huiAudioCorpus.persistenz.AudioPersistenz import AudioPersistenz
from huiAudioCorpus.persistenz.HParamsPersistenz import HParamsPersistenz
from huiAudioCorpus.filter.AudioFilter import AudioFilter
from huiAudioCorpus.persistenz.MelSpectrogramScalerPersistenz import MelSpectrogramScalerPersistenz
from huiAudioCorpus.transformer.MelSpectrogramScalerTransformer import MelSpectrogramScalerTransformer
from huiAudioCorpus.persistenz.CredentialsPersistenz import CredentialsPersistenz
from huiAudioCorpus.workflows.trainWorkflow.Step1_CopyDatasetsToLocal import Step1_CopyDatasetsToLocal
from huiAudioCorpus.transformer.AudioFadeTransformer import AudioFadeTransformer
from normalizer.normalizer import Normalizer
from huiAudioCorpus.workflows.TextAndAudioStatisticWorkflow import TextAndAudioStatisticWorkflow
import ttsCode.testData.speaker as libraryPathModule

import credentials as credentials

import inspect

disableLog()


defaultConfig = {
    'audioAddSilenceTransformer': {
        'endDurationSeconds': 0.7,
        'startDurationSeconds': 0
    },
    'sentenceToPhoneticSentenceConverter': {
        'libraryPath': list(libraryPathModule.__path__)[0] + '/phonemeLibraryGerman.csv'
    },
    'credentialsPersistenz': {
        'path': list(credentials.__path__)[0] + '/credentials.json'
    },
    'listToHistogramConverter': {
        'stepSize':1
    }
}

class DependencyInjection:
    #Extern
    normalizer: Normalizer
    #Calculators
    audioFromMelSpectrogramSpeackerCallculator:AudioFromMelSpectrogramSpeackerCallculator
    melSpectrogramFromSymbolSentenceSpeakerCallculator:MelSpectrogramFromSymbolSentenceSpeakerCallculator
    alignSentencesIntoTextCalculator: AlignSentencesIntoTextCalculator

        
    #Components
    sentencesToAudioComponent:SentencesToAudioComponent
    audioStatisticComponent: AudioStatisticComponent
    textStatisticComponent: TextStatisticComponent

    #Converters
    audioToParallelWaveGanMelSpectrogramConverter:AudioToParallelWaveGanMelSpectrogramConverter
    audioToPowerMelSpectrogramConverter:AudioToPowerMelSpectrogramConverter
    phoneticSentenceToSymbolSentenceConverter:PhoneticSentenceToSymbolSentenceConverter
    sentenceToPhoneticSentenceConverter:SentenceToPhoneticSentenceConverter
    transcriptsToSentencesConverter:TranscriptsToSentencesConverter
    listToStatisticConverter:ListToStatisticConverter
    listToHistogramConverter: ListToHistogramConverter
    stringToSentencesConverter: StringToSentencesConverter
    audioToSentenceConverter: AudioToSentenceConverter


    #Filters
    audioFilter:AudioFilter
    
    #Persistence
    audioPersistenz:AudioPersistenz
    audioTranscriptPairPersistenz:AudioTranscriptPairPersistenz
    melSpectrogramScalerPersistenz:MelSpectrogramScalerPersistenz
    transcriptsPersistenz:TranscriptsPersistenz
    credentialsPersistenz: CredentialsPersistenz
    yamlPersistenz:YamlPersistenz
    hParamsPersistenz:HParamsPersistenz
    audiosFromLibrivoxPersistenz:AudiosFromLibrivoxPersistenz
    GutenbergBookPersistenz: GutenbergBookPersistenz
    
    #Transformers
    audioAddSilenceTransformer:AudioAddSilenceTransformer
    audioSamplingRateTransformer:AudioSamplingRateTransformer
    melSpectrogramScalerTransformer:MelSpectrogramScalerTransformer
    speakerPersistenz:SpeakerPersistenz
    transcriptsSelectionTransformer:TranscriptsSelectionTransformer
    parallelWaveGanConfigTransformer:ParallelWaveGanConfigTransformer
    glowTtsConfigTransformer:GlowTtsConfigTransformer
    audioSplitTransformer: AudioSplitTransformer
    sentenceDistanceTransformer: SentenceDistanceTransformer
    audioLoudnessTransformer: AudioLoudnessTransformer
    audioFadeTransformer: AudioFadeTransformer


    #Utilities
    pathUtil:PathUtil
    fileListUtil: FileListUtil
    secureFTP: SecureFTP

    #Workflows
    resampleCopyFilterAudioWorkflow:ResampleCopyFilterAudioWorkflow
    step0_Overview: Step0_Overview
    step1_CopyDatasetsToLocal: Step1_CopyDatasetsToLocal
    step1_DownloadAudio: Step1_DownloadAudio
    step2_SplitAudio: Step2_SplitAudio
    step2_1_AudioStatistic: Step2_1_AudioStatistic
    step3_DowloadText: Step3_DownloadText
    step3_1_PrepareText: Step3_1_PrepareText
    step4_TranscriptAudio: Step4_TranscriptAudio
    step5_AlignText: Step5_AlignText
    step6_FinalizeDataset: Step6_FinalizeDataset
    step7_AudioRawStatistic: Step7_AudioRawStatistic
    step8_DatasetStatistic: Step8_DatasetStatistic
    step9_GenerateCleanDataset: Step9_GenerateCleanDataset

    textAndAudioStatisticWorkflow: TextAndAudioStatisticWorkflow

    #plot
    plot: Plot
    
    def __init__(self, config={}):
        configWithDefault = defaultConfig.copy()
        configWithDefault.update(config)
        self.allClassReferences = self.getAllClassReferences(configWithDefault)
        initialedClasses = {}
        for name, classInstance in self.allClassReferences.items():
            def getLambda (name, classInstance):
                return property(lambda _: self.initClass(name, classInstance, self.classConstructor, initialedClasses, configWithDefault, name ))
            setattr(DependencyInjection, name, getLambda(name, classInstance))

    def initClass(self, className, classReference , classConstructorMethod, initialedClasses, config , requestedClass = ''):
        if className in initialedClasses:
            return initialedClasses[className]
        arguments = self.getConstructorReferenceClasses(classReference)
        for argument in arguments:
            if argument not in initialedClasses.values() and arguments[argument] is not None:
                self.initClass(argument, arguments[argument], classConstructorMethod, initialedClasses, config, requestedClass)
        
        classConfig = config[className].copy() if className in config else {}
        if '#' in classConfig:
            classConfig.pop('#')
        classConfig
        try:

            newClassInstance = classConstructorMethod(classReference, initialedClasses, classConfig)
        except Exception as e:
            raise DependencyInjectionError(e, classConfig, classReference.__name__, requestedClass)
        initialedClasses[className] = newClassInstance
        return newClassInstance


    def classConstructor(self,classReference, initialedClasses , classConfig):
        classConstructor = classConfig.copy()
        references = self.getConstructorReferenceClasses(classReference)
        for ref in references:
            if references[ref] is not None:
                classConstructor[ref] = initialedClasses[ref]
        classInstance = classReference(**classConstructor)

        return classInstance

    def getConstructorReferenceClasses(self, classReference):
        arguments = self.getAllConstructorArguments(classReference)

        references = {}
        for argument in arguments:
            if argument in ["self","args","kwargs"]:
                continue
            references[argument] = self.allClassReferences[argument] if argument in self.allClassReferences.keys() else None
        return references

    def getAllConstructorArguments(self, classInstance):
        return list(inspect.signature(classInstance.__init__).parameters.keys())

    def getAllClassReferences(self,configWithDefault):
        classes = globalClassesAtImportTime.copy()
        for className in configWithDefault:
            if '#' in configWithDefault[className]:
                classes[className] = configWithDefault[className]['#']
        return classes


globalClassesAtImportTime = DependencyInjection.__dict__.get("__annotations__")
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

from ttsCode.src.workflows.createDatasetWorkflow.Step8_DatasetStatistic import Step8_DatasetStatistic
from ttsCode.src.workflows.createDatasetWorkflow.Step9_GenerateCleanDataset import Step9_GenerateCleanDataset
from ttsCode.src.workflows.createDatasetWorkflow.Step7_AudioRawStatistic import Step7_AudioRawStatistic
from ttsCode.src.workflows.createDatasetWorkflow.Step3_1_PrepareText import Step3_1_PrepareText
from ttsCode.src.workflows.createDatasetWorkflow.Step0_Overview import Step0_Overview
from ttsCode.src.workflows.createDatasetWorkflow.Step2_1_AudioStatistic import Step2_1_AudioStatistic
from ttsCode.src.workflows.createDatasetWorkflow.Step6_FinalizeDataset import Step6_FinalizeDataset
from ttsCode.src.transformer.SentenceDistanceTransformer import SentenceDistanceTransformer
from ttsCode.src.calculator.AlignSentencesIntoTextCalculator import AlignSentencesIntoTextCalculator
from ttsCode.src.workflows.createDatasetWorkflow.Step5_AlignText import Step5_AlignText
from ttsCode.src.converter.AudioToSentenceConverter import AudioToSentenceConverter
from ttsCode.src.workflows.createDatasetWorkflow.Step4_TranscriptAudio import Step4_TranscriptAudio
from ttsCode.src.persistenz.GutenbergBookPersistenz import GutenbergBookPersistenz
from ttsCode.src.workflows.createDatasetWorkflow.Step3_DownloadText import Step3_DownloadText
from ttsCode.src.transformer.AudioSplitTransformer import AudioSplitTransformer
from ttsCode.src.transformer.AudioLoudnessTransformer import AudioLoudnessTransformer
from ttsCode.src.workflows.createDatasetWorkflow.Step2_SplitAudio import Step2_SplitAudio
from ttsCode.src.persistenz.AudiosFromLibrivoxPersistenz import AudiosFromLibrivoxPersistenz
from ttsCode.src.workflows.createDatasetWorkflow.Step1_DownloadAudio import Step1_DownloadAudio
from ttsCode.src.converter.StringToSentencesConverter import StringToSentencesConverter
from ttsCode.src.transformer.GlowTtsConfigTransformer import GlowTtsConfigTransformer
from frosch import hook
hook(theme = 'paraiso_dark')
import logging
disableLog()

from ttsCode.src.utils.SecureFTP import SecureFTP
from ttsCode.src.transformer.YamlConfigurationTransformer import ParallelWaveGanConfigTransformer
from ttsCode.src.persistenz.YamlPersistenz import YamlPersistenz
from ttsCode.src.error.DependencyInjectionError import DependencyInjectionError
from ttsCode.src.converter.ListToHistogramConverter import ListToHistogramConverter
from ttsCode.src.converter.ListToStatisticConverter import ListToStatisticConverter
from ttsCode.src.ui.Plot import Plot
from ttsCode.src.components.TextStatisticComponent import TextStatisticComponent
from ttsCode.src.components.AudioStatisticComponent import AudioStatisticComponent
from ttsCode.src.converter.AudioToPowerMelSpectrogramConverter import AudioToPowerMelSpectrogramConverter
from ttsCode.src.converter.AudioToParallelWaveGanSpectrogramConverter import AudioToParallelWaveGanMelSpectrogramConverter
from ttsCode.src.utils.PathUtil import PathUtil
from ttsCode.src.utils.FileListUtil import FileListUtil
from ttsCode.src.persistenz.SpeakerPersistenz import SpeakerPersistenz
from ttsCode.src.converter.TranscriptsToSentencesConverter import TranscriptsToSentencesConverter
from ttsCode.src.persistenz.AudioTranscriptPairPersistenz import AudioTranscriptPairPersistenz
from ttsCode.src.components.SentencesToAudioComponent import SentencesToAudioComponent
from ttsCode.src.calculator.AudioFromMelSpectrogramSpeackerCallculator import AudioFromMelSpectrogramSpeackerCallculator
from ttsCode.src.calculator.MelSpectrogramFromSymbolSentenceSpeakerCallculator import MelSpectrogramFromSymbolSentenceSpeakerCallculator
from ttsCode.src.converter.PhoneticSentenceToSymbolSentenceConverter import PhoneticSentenceToSymbolSentenceConverter
from ttsCode.src.converter.SentenceToPhoneticSentenceConverter import SentenceToPhoneticSentenceConverter
from ttsCode.src.transformer.AudioAddSilenceTransformer import AudioAddSilenceTransformer
from ttsCode.src.transformer.TranscriptsSelectionTransformer import TranscriptsSelectionTransformer
from ttsCode.src.workflows.ResampleCopyFilterAudioWorkflow import ResampleCopyFilterAudioWorkflow
from ttsCode.src.transformer.AudioSamplingRateTransformer import AudioSamplingRateTransformer
from ttsCode.src.persistenz.TranscriptsPersistenz import TranscriptsPersistenz
from ttsCode.src.persistenz.AudioPersistenz import AudioPersistenz
from ttsCode.src.persistenz.HParamsPersistenz import HParamsPersistenz
from ttsCode.src.filter.AudioFilter import AudioFilter
from ttsCode.src.persistenz.MelSpectrogramScalerPersistenz import MelSpectrogramScalerPersistenz
from ttsCode.src.transformer.MelSpectrogramScalerTransformer import MelSpectrogramScalerTransformer
from ttsCode.src.persistenz.CredentialsPersistenz import CredentialsPersistenz
from ttsCode.src.workflows.trainWorkflow.Step1_CopyDatasetsToLocal import Step1_CopyDatasetsToLocal
from ttsCode.src.transformer.AudioFadeTransformer import AudioFadeTransformer
from normalizer.normalizer import Normalizer
from ttsCode.src.workflows.TextAndAudioStatisticWorkflow import TextAndAudioStatisticWorkflow
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
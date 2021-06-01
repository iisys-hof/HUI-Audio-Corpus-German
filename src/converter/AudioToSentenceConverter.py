from typing import List
from ttsCode.src.persistenz.AudioPersistenz import AudioPersistenz
from ttsCode.src.transformer.AudioSamplingRateTransformer import AudioSamplingRateTransformer
from sttInference import deepspeechModel
from ttsCode.src.model.Audio import Audio
from ttsCode.src.model.Sentence import Sentence
import numpy as np
from tqdm import tqdm

try:
    from deepspeech import Model
except:
    print('failed to load deepspeech, if you need it, try to install it')

from sttInference import deepspeechModel

class AudioToSentenceConverter:
    def __init__(self):
        self.modelPath = deepspeechModel.__path__[0]
        self.model = None
        

    def convert(self, audio: Audio, samplingRate:int = 15000):
        if self.model is None:
            self.model, self.samplingRate = self.loadDeepspeech(self.modelPath)
        audioSamplingRateTransformer = AudioSamplingRateTransformer(self.samplingRate)
        audioSampled = audioSamplingRateTransformer.transform(audio)
        timeSeries =  audioSampled.timeSeries
        timeSeries /=1.414
        timeSeries *= 32767
        audioNumpy = timeSeries.astype(np.int16)

        transcript = self.model.stt(audioNumpy)
        sentence = Sentence(transcript, audio.id)
        return sentence

    def loadDeepspeech(self, modelPath: str):
        model = Model(modelPath+"/output_graph.pb")
        model.enableExternalScorer(modelPath+"/kenlm.scorer")
        desiredSamplingRate = model.sampleRate()
        return model, desiredSamplingRate


if __name__ == "__main__":
    import librosa
    path = '/media/ppuchtler/LangsameSSD/Projekte/textToSpeech/datasetWorkflow/Step2_SplitAudio/audio/'
    
    addAudio = AudioPersistenz(path).load('acht_gesichter_am_biwasee_01_f000177')
    audio = AudioPersistenz(path).load('acht_gesichter_am_biwasee_01_f000077')

    audio = AudioPersistenz(path).load('acht_gesichter_am_biwasee_01_f000030')
    audio1 = AudioPersistenz(path).load('acht_gesichter_am_biwasee_01_f000105')
    audio = AudioPersistenz(path).load('acht_gesichter_am_biwasee_01_f000166')

    #audioRemove = AudioPersistenz(path).load('acht_gesichter_am_biwasee_01_f000001')
    #audio = AudioAddSilenceTransformer(10, 10).transform(audio)
    #audio = audio + audio

    converter = AudioToSentenceConverter() 
    transcript = converter.convert(addAudio +audio + addAudio)

    print(transcript.sentence)
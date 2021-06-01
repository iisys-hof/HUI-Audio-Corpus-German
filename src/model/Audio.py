import numpy as np
from numpy.lib.function_base import average
from ttsCode.src.utils.ModelToStringConverter import ToString
from nptyping import NDArray
import pyloudnorm as pyln
import librosa

class Audio(ToString):
    def __init__(self, audioTimeSeries: NDArray, samplingRate:  int, id: str, name: str):
        self.timeSeries = audioTimeSeries
        self.samplingRate = samplingRate
        self.name = name
        self.id = id


    @property
    def samples(self)->int:
        return self.timeSeries.shape[0]

    @property
    def duration(self)-> float:
        return self.samples/ self.samplingRate


    def __add__(self, other: 'Audio') -> 'Audio':
        audioTimeSeries = self.timeSeries.tolist() + other.timeSeries.tolist()
        audioTimeSeries = np.array(audioTimeSeries)
        id = self.id + '&' + other.id
        name = self.name + '&' + other.name
        
        samplingRateSelf = self.samplingRate
        samplingRateOther = other.samplingRate
        if samplingRateOther != samplingRateSelf:
            raise ValueError(f"The samplingrates from the audio files are different sr1: {samplingRateSelf} sr2: {samplingRateOther} from the audio files with the combined id: {id} and name: {name}")

        audio = Audio(audioTimeSeries,samplingRateSelf, id, name)
        return audio

    def __radd__(self, other):
        return self

    @property
    def loudness(self)->float:
        meter = pyln.Meter(self.samplingRate) # create BS.1770 meter
        loudness = meter.integrated_loudness(self.timeSeries) 
        return loudness

    @property
    def silenceDB(self)->float:
        silenceDurationInSeconds= 0.05
        frameLength = int(silenceDurationInSeconds* self.samplingRate)
        for silenceDezibel in range(100, 1,-1):
            splitted = librosa.effects.split(self.timeSeries,silenceDezibel , frame_length=frameLength, hop_length=int(frameLength/4))
            if len(splitted)>1:
                return -silenceDezibel
        return 0
    
    @property
    def silencePercent(self)->float:
        states = self.isLoud()
        silencePercent = 1- sum(states)/len(states)
        return silencePercent

    def isLoud(self):
        #https://librosa.org/doc/latest/auto_examples/plot_viterbi.html#sphx-glr-auto-examples-plot-viterbi-py
        rms = librosa.feature.rms(y=self.timeSeries)[0]# type: ignore

        r_normalized = (rms - 0.02) / np.std(rms)
        p = np.exp(r_normalized) / (1 + np.exp(r_normalized))# type: ignore


        transition = librosa.sequence.transition_loop(2, [0.5, 0.6])
        full_p = np.vstack([1 - p, p])
        states = librosa.sequence.viterbi_discriminative(full_p, transition)
        return states

    @property
    def averageFrequency(self)->float:
        try:
            cent = librosa.feature.spectral_centroid(y=self.timeSeries, sr=self.samplingRate)[0] #type: ignore
            loudPositions = self.isLoud()

            centAtLoud = [cent[index] for index in range(len(cent)) if loudPositions[index]==1]
            averageFrequency = round(average(centAtLoud)) #type: ignore
            return averageFrequency
        except:
            return -1

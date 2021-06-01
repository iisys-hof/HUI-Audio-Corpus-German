
from ttsCode.src.model.Audio import Audio
from pandas.core.frame import DataFrame
from ttsCode.src.converter.ListToHistogramConverter import ListToHistogramConverter
from ttsCode.src.converter.ListToStatisticConverter import ListToStatisticConverter
from ttsCode.src.persistenz.AudioPersistenz import AudioPersistenz
from joblib import Parallel, delayed

class AudioStatisticComponent:
    def __init__(self, audioPersistenz: AudioPersistenz, listToStatisticConverter:ListToStatisticConverter, listToHistogramConverter: ListToHistogramConverter):
        self.audioPersistenz = audioPersistenz
        self.listToStatisticConverter = listToStatisticConverter
        self.listToHistogramConverter = listToHistogramConverter
        self.columns = ['id','duration', 'loudness', 'minSilenceDB', 'samplingrate', 'silencePercent', 'averageFrequency' ]

    def run(self):
        rawData = self.loadAudioFiles()
        return self.getStatistic(rawData)

    def getStatistic(self, rawData):
        descriptions = ['Length in seconds', 'Loudness in DB', 'Minimum silence in DB', 'Samplingrate in Hz', 'Silence in percent', 'Average Frquency in Hz']
        statistics = {}
        for column in rawData:
            if column not in self.columns:
                continue
            statistics[column] = {
                'name': column,
                'statistic': self.listToStatisticConverter.convert(rawData[column].tolist()),
                'histogram': self.listToHistogramConverter.convert(rawData[column].tolist()),
                'description': descriptions[len(statistics)]
            }

        return statistics, rawData

    def loadAudioFiles(self):
        result = Parallel(n_jobs=12, verbose=10, batch_size=100)(delayed(self.loadAudio)(audio) for audio in self.audioPersistenz.getIds())
        rawData = DataFrame(result, columns  = self.columns)
        rawData = rawData.set_index('id')
        return rawData

    def loadAudio(self, audioId: str):
        audio = self.audioPersistenz.load(audioId)
        return [audio.id.split("\\")[-1].split("/")[-1], round(audio.duration,1), round(audio.loudness,1), round(audio.silenceDB,1), audio.samplingRate, round(audio.silencePercent*100), round(audio.averageFrequency)]

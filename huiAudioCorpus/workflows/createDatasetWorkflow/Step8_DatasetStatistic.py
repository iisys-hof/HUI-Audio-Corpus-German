from huiAudioCorpus.utils.DoneMarker import DoneMarker
from huiAudioCorpus.utils.PathUtil import PathUtil
import pandas as pd
from huiAudioCorpus.components.AudioStatisticComponent import AudioStatisticComponent
from huiAudioCorpus.components.TextStatisticComponent import TextStatisticComponent
from typing import List
from huiAudioCorpus.ui.Plot import Plot
from pandas_profiling import ProfileReport

class Step8_DatasetStatistic:
    def __init__(self, savePath: str, loadPath: str, specialSpeackers: List[str], filter,  pathUtil: PathUtil, audioStatisticComponent:AudioStatisticComponent, textStatisticComponent:TextStatisticComponent, plot: Plot):
        self.savePath = savePath
        self.pathUtil = pathUtil
        self.loadPath = loadPath
        self.specialSpeackers = specialSpeackers
        self.filter = filter
        self.audioStatisticComponent =audioStatisticComponent
        self.textStatisticComponent = textStatisticComponent
        self.plot = plot

    def run(self):
        doneMarker = DoneMarker(self.savePath)
        result = doneMarker.run(self.script, deleteFolder=False)
        return result

    def script(self):
        rawData = pd.read_csv(self.loadPath, sep='|', index_col='id')

        print('Audios bevore: ', rawData.shape[0])
        infoText = " - full"
        if self.filter is not None:
            infoText = " - clean"
            rawData = self.filter(rawData)
        print('Audios after: ', rawData.shape[0])


        print(rawData)
        # all Speakers
        self.saveSummary(rawData, self.savePath  + '/complete', "All speakers" + infoText)

        # every Speacker
        for speackerId, data in rawData.groupby('speacker'):
            self.saveSummary(data, self.savePath + '/speacker/' + speackerId, "Speaker: " + speackerId + infoText)

        # others
        others = rawData[~rawData['speacker'].isin(self.specialSpeackers)]
        self.saveSummary(others, self.savePath + '/others', "Other speakers" + infoText)


    def saveSummary(self, rawData, savePath: str, title: str):
        print(title)
        statisticsText, _, counter, uniqeWordsWithMinimum = self.textStatisticComponent.getStatistic(rawData)
        statisticsAudio, _ = self.audioStatisticComponent.getStatistic(rawData)

        statistics = {**statisticsAudio, **statisticsText}
        filePath = savePath + '/statistic.txt'
        self.pathUtil.createFolderForFile(filePath)

        rawData.to_csv(savePath + '/overview.csv' , sep='|')

        profile = rawData.profile_report(title = title)
        profile.to_file(savePath + "/profilingReport.html")


        self.pathUtil.saveJson(savePath + '/wordCounts.json',counter )
        self.pathUtil.saveJson(savePath + '/uniqueWordsWithMinimalNumberOfOccurrences.json',uniqeWordsWithMinimum )

        with open(filePath, 'w') as textFile:
            for statistic in statistics.values():
                textFile.write(statistic['description'])
                textFile.write('\n')
                textFile.write(statistic['statistic'].__str__())
                textFile.write('\n')
                textFile.write('\n')
                textFile.write('\n')

        histogrammData = {}
        extractHistogram = lambda hist : {'bins': hist.bins, 'values': hist.values}

        for statistic in statistics.values():
            if statistic['name'] =='samplingrate':
                continue
            self.plot.histogram(statistic['histogram'],  statistic['description'])
            self.plot.savePath = savePath
            self.plot.save(statistic['name'])
            histogrammData[statistic['name']] = extractHistogram(statistic['histogram'])

        self.pathUtil.saveJson(savePath + '/histogrammData.json',histogrammData )
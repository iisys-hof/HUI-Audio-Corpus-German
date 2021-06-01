from ttsCode.src.utils.DoneMarker import DoneMarker
from ttsCode.src.components.AudioStatisticComponent import AudioStatisticComponent
from ttsCode.src.ui.Plot import Plot


class Step2_1_AudioStatistic:
    def __init__(self, savePath: str, audioStatisticComponent: AudioStatisticComponent, plot: Plot):
        self.savePath = savePath
        self.audioStatisticComponent = audioStatisticComponent
        self.plot = plot

    def run(self):
        doneMarker = DoneMarker(self.savePath)
        result = doneMarker.run(self.script, deleteFolder=False)
        return result

    def script(self):
        statistics, rawData = self.audioStatisticComponent.run()

        self.plot.histogram(statistics['duration']['histogram'],  statistics['duration']['description'])
        self.plot.save('audioLength')
        self.plot.show()

        with open(self.savePath + '/statistic.txt', 'w') as textFile:
            for statistic in statistics.values():
                print(statistic['description'])
                print(statistic['statistic'])
                textFile.write(statistic['description'])
                textFile.write('\n')
                textFile.write(statistic['statistic'].__str__())
                textFile.write('\n')

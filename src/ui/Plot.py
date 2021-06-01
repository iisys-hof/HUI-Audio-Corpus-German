import matplotlib.pyplot as plt
from ttsCode.src.model.Histogram import Histogram
from ttsCode.src.utils.PathUtil import PathUtil
import logging
logging.getLogger('matplotlib.font_manager').disabled = True
logging.getLogger('matplotlib.colorbar').disabled = True

class Plot:
    def __init__(self, showDuration: int, savePath: str = ''):
        self.showDuration = showDuration
        self.savePath = savePath
        self.pathUtil = PathUtil()


    def histogram(self, histogram:Histogram, name:str, logScaleY = False, logScaleX = False):
        plt.clf()
        _, ax = plt.subplots()


        ax.bar(histogram.bins,histogram.values, width=1) # type: ignore
        ax.set_ylabel('count') # type: ignore
        ax.set_xlabel('bins') # type: ignore
        ax.set_title(name) # type: ignore
        if logScaleY:
            ax.set_yscale('log')
        if logScaleX:
            ax.set_xscale('log')

    def show(self):
        plt.show(block=False)
        plt.pause(self.showDuration)
        plt.close()
    
    def save(self, filename: str):
        filename = self.savePath + '/' + filename
        self.pathUtil.createFolderForFile(filename)
        plt.savefig(filename, dpi=200)

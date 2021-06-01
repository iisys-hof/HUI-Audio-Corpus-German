from ttsCode.src.model.Histogram import Histogram
from typing import List, TypeVar

import numpy as np
number = TypeVar('number', int, float)

class ListToHistogramConverter:
    def __init__(self, stepSize: int):
        self.stepSize =stepSize

    def convert(self, list: List[number]):
        bins = np.arange(round(min(1,min(list)))-1,max(list) + 2*self.stepSize,self.stepSize)
        exportBins: List[number]
        values : List[number]
        valuesNumpy, exportBinsNumpy =  np.histogram(list, bins=bins) # type: ignore
        exportBins = exportBinsNumpy.tolist()# type: ignore
        values = valuesNumpy.tolist()# type: ignore
        histogram = Histogram(exportBins[:-1], values)
        return histogram
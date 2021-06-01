import numpy as np
from huiAudioCorpus.model.Statistic import Statistic

from typing import List, TypeVar

number = TypeVar('number', int, float)

class ListToStatisticConverter:

    def convert(self, list: List[number]):
        count = len(list)
        maximum = max(list)
        minimum = min(list)
        total = sum(list)
        median: float
        median = np.median(list)
        std = np.std(list)
        var = np.var(list)
        average = total/count
        statistic = Statistic(count,maximum,minimum,median,average,total, std, var)
        return statistic
    
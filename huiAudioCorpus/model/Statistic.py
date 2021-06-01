from huiAudioCorpus.utils.ModelToStringConverter import ToString


class Statistic(ToString):
    def __init__(self, count:int, max:float, min:float, median:float, average:float, sum:float, std: float, var: float):
        self.count = count
        self.max = max
        self.min = min
        self.median = median
        self.average = average
        self.sum = sum
        self.std = std
        self.var = var
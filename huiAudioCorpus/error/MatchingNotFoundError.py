from typing import List


class MatchingNotFoundError(Exception):

    def __init__(self, missingIdsIn1: List[str], missingIdsIn2: List[str], namemissingIdsIn1: str, namemissingIdsIn2: str):
        self.missingIdsIn1 = missingIdsIn1
        self.missingIdsIn2 = missingIdsIn2
        self.namemissingIdsIn1= namemissingIdsIn1
        self.namemissingIdsIn2 = namemissingIdsIn2

        super().__init__(f'Missing ids from matching {self.namemissingIdsIn1} and {self.namemissingIdsIn2}')

    def __str__(self):
        return self.getString()

    def getString(self):
        string = f'Exception: Missing ids from matching {self.namemissingIdsIn1} and {self.namemissingIdsIn2}\n'
        string+= f'misssing ids in {self.namemissingIdsIn1}: {self.missingIdsIn1}\n'
        string+= f'misssing ids in {self.namemissingIdsIn2}: {self.missingIdsIn2}\n'
        return string
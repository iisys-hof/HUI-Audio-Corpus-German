from huiAudioCorpus.utils.ModelToStringConverter import ToString

class PhoneticChars(ToString):

    def __init__(self):
        self.chars = ['ˈ', 'a', 'l', 'ə', 's', ' ', 'i', 'ʔ', 'ɛ', 'n', 'd', 'e', 'ː', 'ɐ', '̯', 'v', 't', 'ɪ', 'm', 'j', 'ɔ', 'x', '͡', 'u', ',', 'ʊ', 'z', 'p', 'ʁ', 'o', 'ʃ', 'ç', 'ɡ', '̩', '.', 'k', 'h', 'ˌ', 'f', 'b', 'ŋ', 'y', 'ʏ', 'œ', 'æ', 'ø', '!', 'ʒ', '…', ':', '̍', '?', '̥', '̃', 'r', 'ɑ', 'θ', "'", 'ð', 'ɱ', 'ʙ', 'ɺ', "ˑ", "ɒ",'‿']
    
    @property
    def countChars(self):
        return len(self.chars)

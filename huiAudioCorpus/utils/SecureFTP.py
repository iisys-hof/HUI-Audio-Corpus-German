from huiAudioCorpus.persistenz.CredentialsPersistenz import CredentialsPersistenz
from huiAudioCorpus.utils.PathUtil import PathUtil
import pysftp

# This class is hard to test. Because the risk is not so high i decided not to test this class automatic. Pascal
class SecureFTP:# pragma: no cover
    def __init__(self, pathUtil: PathUtil, server: str, credentialsPersistenz: CredentialsPersistenz):
        cnopts = pysftp.CnOpts()
        credentials = credentialsPersistenz.load(server)
        cnopts.hostkeys = None   
        self.connection =  pysftp.Connection(server, username=credentials.username, password=credentials.password, cnopts=cnopts)
        self.pathUtil = pathUtil

    def getFiles(self, path: str):
        files = self.connection.listdir(path)
        return files

    def copyFile(self, sourcePath: str, targetPath: str):
        source = self.connection.open(sourcePath,'rb')
        self.pathUtil.copyFileWithStream(source, self.getSize(sourcePath), targetPath)# type:ignore
        source.close()

    def getSize(self, sourcePath: str):
        stats = self.connection.stat(sourcePath)
        size = stats.st_size
        return size
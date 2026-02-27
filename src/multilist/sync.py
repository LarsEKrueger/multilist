from multilist import db
import multilist.version as mlv
import requests

class Synchronizer:
    """ Checks a URL for a multilist server.

    If it can't find a server at the given URL, sleep for a while.

    If the server can be contacted, synchronize the databases.
    """

    def __init__(self, remoteUrl):
        self.remoteUrl = remoteUrl
        self.syncSuccess = False

    def checkRemoteVersion(self):
        """ Check if the server at the remote URL replies with the correct name and version. Return true if it worked. """
        result = False
        try:
            resp = requests.get( f"{self.remoteUrl}/version").json()
            if (resp['name'] == mlv.name ) and (resp['version'] == mlv.version):
                result = True
        except:
            pass

        return result

    def synchronize(self, database):
        pass



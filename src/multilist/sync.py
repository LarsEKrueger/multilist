from multilist import db
import multilist.version as mlv
import requests
import json


class Synchronizer:
    """Checks a URL for a multilist server.

    If it can't find a server at the given URL, sleep for a while.

    If the server can be contacted, synchronize the databases.
    """

    def __init__(self, remoteUrl):
        self.remoteUrl = remoteUrl
        self.syncSuccess = False

    def checkRemoteVersion(self):
        """Check if the server at the remote URL replies with the correct name and version. Return true if it worked."""
        result = False
        try:
            resp = requests.get(f"{self.remoteUrl}/version").json()
            if (resp["name"] == mlv.name) and (resp["version"] == mlv.version):
                result = True
        except:
            pass
        return result

    def synchronize(self, database):
        """Synchronize the local database with the remote database. Return false on failures."""
        # Algo
        # * Sync the lists
        #   local       remote      action
        #   exists      doesn't     copy to remove
        #   doesn't     exists      copy to local
        #   exists      exists      copy to db with older last_modified

        # Get lists
        remoteLists = requests.get(f"{self.remoteUrl}/lists").json()
        localLists = database.getLists()

        # Ensure local has what remote has
        for localId in localLists:
            sendToRemote = False
            localData = database.getListProperties(localId)
            if localId in remoteLists:
                remoteData = requests.get(f"{self.remoteUrl}/list/{localId}").json()
                remoteProps = db.SyncListProps.model_validate(remoteData)
                if (remoteProps.last_modified is not None) and (
                    "last_modified" in localData
                ):
                    remoteTime = remoteProps.last_modified
                    localTime = localData["last_modified"]
                    if localTime < remoteTime:
                        database.syncList(
                            localId,
                            remoteTime,
                            remoteProps.name,
                            remoteProps.priority,
                            remoteProps.warning_period,
                        )
                    elif localTime > remoteTime:
                        sendToRemote = True
            else:
                # Local List doesn't exist in remote DB -> Sync it there
                sendToRemote = True
            if sendToRemote:
                resp = requests.post(
                    f"{self.remoteUrl}/syncList/{localId}", data=json.dumps(localData)
                )

        # Ensure that remote has what local has
        for remoteId in remoteLists:
            sendToLocal = False
            remoteData = requests.get(f"{self.remoteUrl}/list/{remoteId}").json()
            remoteProps = db.SyncListProps.model_validate(remoteData)
            if remoteId in localLists:
                # Remote found, compare time
                localData = database.getListProperties(remoteId)
                if (remoteProps.last_modified is not None) and (
                    "last_modified" in localData
                ):
                    remoteTime = remoteProps.last_modified
                    localTime = localData["last_modified"]
                    if localTime < remoteTime:
                        sendToLocal = True
                    elif localTime > remoteTime:
                        resp = requests.post(
                            f"{self.remoteUrl}/syncList/{remoteId}",
                            data=json.dumps(localData),
                        )
            else:
                # Remote not found
                sendToLocal = True
            if sendToLocal:
                database.syncList(
                    remoteId,
                    remoteProps.last_modified,
                    remoteProps.name,
                    remoteProps.priority,
                    remoteProps.warning_period,
                )

        # Go through all lists (should be identical between remote and local now) to sync the items
        localLists = database.getLists()
        for listId in localLists:
            localItems = database.getItems(listId)
            remoteItems = requests.get(f"{self.remoteUrl}/items/{listId}").json()
            # Ensure local has what remote has
            for localId in localItems:
                sendToRemote = False
                localData = database.getItemProperties(listId, localId)
                if localId in remoteItems:
                    # local and remote have it, compare timestamps
                    remoteData = requests.get(
                        f"{self.remoteUrl}/item/{listId}/{localId}"
                    ).json()
                    remoteProps = db.SyncItemProps.model_validate(remoteData)
                    if (remoteProps.last_modified is not None) and (
                        "last_modified" in localData
                    ):
                        remoteTime = remoteProps.last_modified
                        localTime = localData["last_modified"]
                        if localTime < remoteTime:
                            database.syncItem(
                                listId,
                                localId,
                                remoteTime,
                                remoteProps.subject,
                                remoteProps.details,
                                remoteProps.expires,
                                remoteProps.priority,
                                remoteProps.status,
                            )
                        elif localTime > remoteTime:
                            sendToRemote = True
                else:
                    sendToRemote = True
                if sendToRemote:
                    resp = requests.post(
                        f"{self.remoteUrl}/syncItem/{listId}/{localId}",
                        data=json.dumps(localData),
                    )

            # Ensure that remote has what local has
            for remoteId in remoteItems:
                sendToLocal = False
                remoteData = requests.get(
                    f"{self.remoteUrl}/item/{listId}/{remoteId}"
                ).json()
                remoteProps = db.SyncItemProps.model_validate(remoteData)
                if remoteId in localItems:
                    localData = database.getItemProperties(listId, remoteId)
                    if (remoteProps.last_modified is not None) and (
                        "last_modified" in localData
                    ):
                        remoteTime = remoteProps.last_modified
                        localTime = localData["last_modified"]
                        if localTime < remoteTime:
                            sendToLocal = True
                        elif localTime > remoteTime:
                            resp = requests.post(
                                f"{self.remoteUrl}/syncItem{listId}/{remoteId}",
                                data=json.dumps(localData),
                            )
                else:
                    sendToLocal = True

                if sendToLocal:
                    database.syncItem(
                        listId,
                        remoteId,
                        remoteProps.last_modified,
                        remoteProps.subject,
                        remoteProps.details,
                        remoteProps.expires,
                        remoteProps.priority,
                        remoteProps.status,
                    )
        return True

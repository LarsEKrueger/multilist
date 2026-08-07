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
        if self.remoteUrl == "":
            return False
        try:
            print(f"Waiting for {self.remoteUrl} to come online")
            resp = requests.get(f"{self.remoteUrl}/version", timeout=1.0).json()
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

        # Create a session to avoid the DNS lookup for every request
        with requests.Session() as session:

            # Get lists
            remoteLists = session.get(f"{self.remoteUrl}/lists").json()
            remoteDeleted = session.get(f"{self.remoteUrl}/deleted").json()
            localLists = database.getLists()
            localDeleted = database.getDeleted()

            # Ensure local has what remote has
            for localId in localLists:
                # If the local list has been deleted on the remote after the last local change, we delete it locally.
                localData = database.getListProperties(localId)
                if localId in remoteDeleted:
                    if remoteDeleted[localId] > localData["last_modified"]:
                        database.deleteListForce(localId, remoteDeleted[localId])
                        continue
                sendToRemote = False
                if localId in remoteLists:
                    remoteData = session.get(f"{self.remoteUrl}/list/{localId}").json()
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
                                remoteProps
                            )
                        elif localTime > remoteTime:
                            sendToRemote = True
                else:
                    # Local List doesn't exist in remote DB -> Sync it there
                    sendToRemote = True
                if sendToRemote:
                    print(
                        session.post(
                            f"{self.remoteUrl}/syncList/{localId}",
                            json=localData,
                        ).text
                    )

            # Ensure that remote has what local has
            for remoteId in remoteLists:
                remoteData = session.get(f"{self.remoteUrl}/list/{remoteId}").json()
                remoteProps = db.SyncListProps.model_validate(remoteData)
                # If the remote list has been deleted on local after the last remote change, we delete it on the remote.
                if remoteId in localDeleted:
                    if localDeleted[remoteId] > remoteProps.last_modified:
                        resp = session.delete(
                            f"{self.remoteUrl}/syncList/{remoteId}",
                            params={"timestamp": localDeleted[remoteId]},
                        )
                        continue
                sendToLocal = False
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
                            print(
                                session.post(
                                    f"{self.remoteUrl}/syncList/{remoteId}",
                                    json=localData,
                                ).text
                            )
                else:
                    # Remote not found
                    sendToLocal = True
                if sendToLocal:
                    database.syncList( remoteId, remoteProps)

            # Go through all lists (should be identical between remote and local now) to sync the items
            localLists = database.getLists()
            for listId in localLists:
                localItems = database.getItems(listId)
                remoteItems = session.get(f"{self.remoteUrl}/items/{listId}").json()
                # Ensure local has what remote has
                for localId in localItems:
                    localData = database.getItemProperties(listId, localId)

                    # If the local item has been deleted on the remote after the last local change, we delete it locally.
                    if localId in remoteDeleted:
                        if remoteDeleted[localId] > localData["last_modified"]:
                            database.deleteItemForce(
                                listId, localId, remoteDeleted[localId]
                            )
                            continue

                    sendToRemote = False
                    if localId in remoteItems:
                        # local and remote have it, compare timestamps
                        remoteData = session.get(
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
                        print(
                            session.post(
                                f"{self.remoteUrl}/syncItem/{listId}/{localId}",
                                json=localData,
                            ).text
                        )

                # Ensure that remote has what local has
                for remoteId in remoteItems:
                    sendToLocal = False
                    remoteData = session.get(
                        f"{self.remoteUrl}/item/{listId}/{remoteId}"
                    ).json()
                    remoteProps = db.SyncItemProps.model_validate(remoteData)
                    # If the remote item has been deleted on local after the last remote change, we delete it on the remote.
                    if remoteId in localDeleted:
                        if localDeleted[remoteId] > remoteProps.last_modified:
                            session.delete(
                                f"{self.remoteUrl}/syncItem/{listId}/{remoteId}",
                                params={"timestamp": localDeleted[remoteId]},
                            )
                            continue
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
                                print(
                                    session.post(
                                        f"{self.remoteUrl}/syncItem{listId}/{remoteId}",
                                        json=localData,
                                    ).text
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

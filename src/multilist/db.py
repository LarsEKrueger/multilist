# Database abstraxction class for multilist application server

import json
import uuid
import os.path
import time
from pydantic import BaseModel


def _updateDict_(d, field, value):
    """Update the field in the dict if value is not None"""
    if value is not None:
        d[field] = value


def _updateHashDict_(hashDict, item):
    """Create a new uuid and insert the item into the dict. Should the uuid
    already exist, retry until it succeeds. This will eventually happen, as
    uuid1 is time-based."""
    while True:
        ident = uuid.uuid1().hex
        if ident not in hashDict:
            hashDict[ident] = item
            return


def _modifiedNow_(data):
    """Set the last_modified of the give item to the current time"""
    data["last_modified"] = time.time_ns()


def _copyProps_(data, props):
    """Return a new dictionary containing only the given keys"""
    result = {}
    for p in props:
        if p in data:
            result[p] = data[p]
    return result


class ListProps(BaseModel):
    name: str | None = None
    priority: int | None = None
    warning_period: str | None = None


class SyncListProps(ListProps):
    last_modified: int = None


class ItemProps(BaseModel):
    subject: str | None = None
    details: str | None = None
    expires: str | None = None
    priority: int | None = None
    status: str | None = None


class SyncItemProps(ItemProps):
    last_modified: int = None


class Database:
    """Abstracts all database operations into a class API"""

    def __init__(self, path):
        """Construct the DB object

        path: Folder where the DB shall be stored. Folder must exist.

        Format:
        [
          "<uuid of list>": {
            "name": "<name of the list>",
            "priority": <priority as int>,
            "warning_period": <warning period as ISO period>
            "items": {
                  "<uuid of item>": {
                    "subject": "<subject string>",
                    "details": "<detail text>",
                    "expires": <expiration data as ISO date or empty string>,
                    "priority": <priority as int>,
                    "status": <status as string>
                  },
                  "<uuid of item>": {
                    ...
                  },
                  ...
            }
          },
          "<uuid of list>": {
            ...
          }
        ]
        """
        self.path = path

        self.data = {}
        # Load the DB if it exists or create an empty one
        try:
            with open(self.path, "rt") as f:
                self.data = json.load(f)
        except:
            # TODO: Logging
            pass

    def _write_(self):
        """Internal function to write the DB to disk."""
        with open(self.path, "wt") as f:
            json.dump(self.data, f)

    # ---------- List API ----------
    def addList(self):
        """Add an empty list"""
        newList = {
            "name": "New List",
            "warning_period": "1w",
            "last_modified": time.time_ns(),
        }
        _updateHashDict_(self.data, newList)
        self._write_()

    def deleteList(self, listId):
        """Delete a list. Throws if list has items in it."""
        if ("items" in self.data[listId]) and len(self.data[listId]["items"]) != 0:
            # TODO: Define user exception
            raise Exception
        del self.data[listId]

    def updateList(
        self,
        listId,
        name: str = None,
        priority: int = None,
        warning_period: str = None,
    ):
        """Update the fields of a particular list. Only change those fields that are not None."""
        data = self.data[listId]
        _updateDict_(data, "name", name)
        _updateDict_(data, "priority", priority)
        _updateDict_(data, "warning_period", warning_period)
        _modifiedNow_(data)
        self._write_()

    def syncList(
        self,
        listId,
        last_modified: int,
        name: str = None,
        priority: int = None,
        warning_period: str = None,
    ):
        if not listId in self.data:
            self.data[listId] = {}
        data = self.data[listId]
        _updateDict_(data, "name", name)
        _updateDict_(data, "priority", priority)
        _updateDict_(data, "warning_period", warning_period)
        _updateDict_(data, "last_modified", last_modified)
        self._write_()

    def getLists(self):
        """Returns an array of list ids."""
        return [k for k in self.data.keys()]

    def getListProperties(self, listId):
        """Return a dict of list properties."""
        return _copyProps_(
            self.data[listId], ["name", "warning_period", "last_modified", "priority"]
        )

    # ---------- item API ----------
    def addItem(self, listId):
        """Add an item to the given list."""
        newItem = {"subject": "New item", "last_modified": time.time_ns()}
        data = self.data[listId]
        if not "items" in data:
            data["items"] = {}
        _updateHashDict_(data["items"], newItem)
        self._write_()

    def deleteItem(self, listId, itemId):
        """Delete an item from the given list."""
        del self.data[listId]["items"][itemId]
        self._write_()

    def updateItem(
        self,
        listId,
        itemId,
        subject: str = None,
        details: str = None,
        expires: str = None,
        priority: int = None,
        status: str = None,
    ):
        """Update the fields of a particular item.  Only change those fields that are not None."""
        data = self.data[listId]["items"][itemId]
        _updateDict_(data, "subject", subject)
        _updateDict_(data, "details", details)
        _updateDict_(data, "expires", expires)
        _updateDict_(data, "priority", priority)
        _updateDict_(data, "status", status)
        _modifiedNow_(data)
        self._write_()

    def syncItem(
        self,
        listId,
        itemId,
        last_modified: int,
        subject: str = None,
        details: str = None,
        expires: str = None,
        priority: int = None,
        status: str = None,
    ):
        """Update the fields of a particular item.  Only change those fields that are not None."""
        if not "items" in self.data[listId]:
            self.data[listId]["items"] = {}
        if not itemId in self.data[listId]["items"]:
            self.data[listId]["items"][itemId] = {}
        data = self.data[listId]["items"][itemId]
        _updateDict_(data, "subject", subject)
        _updateDict_(data, "details", details)
        _updateDict_(data, "expires", expires)
        _updateDict_(data, "priority", priority)
        _updateDict_(data, "status", status)
        _updateDict_(data, "last_modified", last_modified)
        self._write_()

    def getItems(self, listId):
        """Return a list of itemIds in a particular list."""
        if not "items" in self.data[listId]:
            return []
        return [k for k in self.data[listId]["items"].keys()]

    def getItemProperties(self, listId, itemId):
        """Return a dict of item properties for the given item in the given list."""
        return _copyProps_(
            self.data[listId]["items"][itemId],
            ["subject", "details", "expires", "priority", "status", "last_modified"],
        )

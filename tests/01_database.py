# Test the database

import unittest
from multilist import db
import sys
import pathlib
import json

gDbPath = None


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Get the path to the db from the command line"""
        self.db = db.Database(gDbPath)

    def tearDown(self):
        """Clear the DB instance"""
        try:
            pathlib.Path(self.db.path).unlink()
        except:
            pass
        self.db = None

    def test_addList(self):
        self.assertEqual(len(self.db.getLists()), 0)
        self.db.addList()
        self.assertEqual(len(self.db.getLists()), 1)

    def test_deleteList(self):
        self.assertEqual(len(self.db.getLists()), 0)
        self.db.addList()
        listId = self.db.getLists()[0]
        self.db.deleteList(listId)
        self.assertEqual(len(self.db.getLists()), 0)

    def test_listUpdateName(self):
        self.assertEqual(len(self.db.getLists()), 0)
        self.db.addList()
        listIdOld = self.db.getLists()[0]
        self.db.updateList(listIdOld, name="IAmAList")
        listIdNew = self.db.getLists()[0]
        listProp = self.db.getListProperties(listIdNew)
        self.assertEqual(listProp["name"], "IAmAList")
        self.assertNotEqual(listIdNew, listIdOld)

    def test_listUpdateAll(self):
        self.assertEqual(len(self.db.getLists()), 0)
        self.db.addList()
        listIdOld = self.db.getLists()[0]
        self.db.updateList(listIdOld, name="IAmAList", priority=42, warning_period="D2")
        listIdNew = self.db.getLists()[0]
        listProp = self.db.getListProperties(listIdNew)
        self.assertEqual(listProp["name"], "IAmAList")
        self.assertEqual(listProp["priority"], 42)
        self.assertEqual(listProp["warning_period"], "D2")
        self.assertNotEqual(listIdNew, listIdOld)

    def test_addItem(self):
        self.assertEqual(len(self.db.getLists()), 0)
        self.db.addList()
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 0)
        self.db.addItem(listId)
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 1)

    def test_deleteItem(self):
        self.assertEqual(len(self.db.getLists()), 0)
        self.db.addList()
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 0)
        self.db.addItem(listId)
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 1)
        itemId = self.db.getItems(listId)[0]
        self.db.deleteItem(listId, itemId)
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 0)

    def test_updateItem1(self):
        self.assertEqual(len(self.db.getLists()), 0)
        self.db.addList()
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 0)
        self.db.addItem(listId)
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 1)
        itemId = self.db.getItems(listId)[0]
        self.db.updateItem(listId, itemId, subject="IAmASubject")
        listId = self.db.getLists()[0]
        itemId = self.db.getItems(listId)[0]
        itemProp = self.db.getItemProperties(listId, itemId)
        self.assertEqual(itemProp["subject"], "IAmASubject")

    def test_updateItemAll(self):
        self.assertEqual(len(self.db.getLists()), 0)
        self.db.addList()
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 0)
        self.db.addItem(listId)
        listId = self.db.getLists()[0]
        self.assertEqual(len(self.db.getItems(listId)), 1)
        itemId = self.db.getItems(listId)[0]
        self.db.updateItem(
            listId,
            itemId,
            subject="IAmASubject",
            details="IHaveDetails",
            expires="P18",
            priority=42,
            status="open",
        )
        listId = self.db.getLists()[0]
        itemId = self.db.getItems(listId)[0]
        itemProp = self.db.getItemProperties(listId, itemId)
        self.assertEqual(itemProp["subject"], "IAmASubject")
        self.assertEqual(itemProp["details"], "IHaveDetails")
        self.assertEqual(itemProp["expires"], "P18")
        self.assertEqual(itemProp["priority"], 42)
        self.assertEqual(itemProp["status"], "open")


if __name__ == "__main__":
    gDbPath = sys.argv[1]
    del sys.argv[1]
    unittest.main()

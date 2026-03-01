#! /usr/bin/python3

# Script to test the synchronisation

from multilist import db, sync

database = db.Database("test.json")
synchronizer = sync.Synchronizer("http://localhost:8000")

if synchronizer.checkRemoteVersion():
    print("server found")
else:
    print("server not found")

synchronizer.synchronize(database)

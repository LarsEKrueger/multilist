#! /usr/bin/python3

from multilist import db, sync
import multilist.version as mlv
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic_settings import BaseSettings

import asyncio
from contextlib import asynccontextmanager


class AppSettings(BaseSettings):
    ML_DB_JSON: str = "multilist.json"
    ML_SYNC_URL: str = "http://localhost:8001"


app_settings = AppSettings()

print( f"ML_DB_JSON={app_settings.ML_DB_JSON}")
print( f"ML_SYNC_URL={app_settings.ML_SYNC_URL}")

database = db.Database(app_settings.ML_DB_JSON)


async def backgroundSync():
    """Function to run in the background. It will periodically connect to other servers and synchronize the databases."""
    synchronizer = sync.Synchronizer(app_settings.ML_SYNC_URL)
    while True:
        # Try to sync with the server once a minute.
        while not synchronizer.checkRemoteVersion():
            print( f"Waiting for {app_settings.ML_SYNC_URL} to come online")
            await asyncio.sleep(60)
        print( "Starting sync")
        synchronizer.synchronize(database)
        print( "Sync done. Waiting 30 minutes.")
        await asyncio.sleep(30*60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(backgroundSync())
    yield



app = FastAPI(lifespan=lifespan)


def serveFile(filename, mediaType):
    # TODO: Use install folder
    with open(filename, "rt") as f:
        s = f.read()
    return Response(s, media_type=mediaType)


@app.get("/")
@app.get("/index.html")
async def root():
    return serveFile("html/app.html", "text/html")


@app.get("/jquery.js")
async def jquery():
    return serveFile("jquery/jquery-4.0.0.min.js", "application/javascript")


@app.get("/version")
async def version():
    return {"name": mlv.name, "version": mlv.version}


@app.get("/lists")
async def getLists():
    return database.getLists()


@app.post("/lists")
async def addList():
    database.addList()
    return {}


@app.put("/list/{listId}")
async def updateList(listId: str, listProps: db.ListProps):
    database.updateList(
        listId, listProps.name, listProps.priority, listProps.warning_period
    )
    return {}


@app.post("/syncList/{listId}")
async def syncList(listId: str, listProps: db.SyncListProps):
    print(listProps)
    database.syncList(
        listId,
        listProps.last_modified,
        listProps.name,
        listProps.priority,
        listProps.warning_period,
    )
    return {}


@app.delete("/list/{listId}")
async def deleteList(listId: str):
    try:
        database.deleteList(listId)
    except Exception:
        return False
    return True


@app.get("/list/{listId}")
async def listProps(listId: str):
    return database.getListProperties(listId)


@app.get("/items/{listId}")
async def items(listId: str):
    return database.getItems(listId)


@app.get("/item/{listId}/{itemId}")
async def itemProp(listId: str, itemId: str):
    return database.getItemProperties(listId, itemId)


@app.delete("/item/{listId}/{itemId}")
async def itemProp(listId: str, itemId: str):
    return database.deleteItem(listId, itemId)


@app.post("/items/{listId}")
async def addItem(listId: str):
    database.addItem(listId)


@app.put("/item/{listId}/{itemId}")
async def updateItem(listId: str, itemId: str, itemProps: db.ItemProps):
    database.updateItem(
        listId,
        itemId,
        itemProps.subject,
        itemProps.details,
        itemProps.expires,
        itemProps.priority,
        itemProps.status,
    )
    return {}


@app.post("/syncItem/{listId}/{itemId}")
async def syncItem(listId: str, itemId: str, itemProps: db.SyncItemProps):
    database.syncItem(
        listId,
        itemId,
        itemProps.last_modified,
        itemProps.subject,
        itemProps.details,
        itemProps.expires,
        itemProps.priority,
        itemProps.status,
    )
    return {}


#   @app.middleware("http")
#   async def middleware(request: Request, call_next):
#       try:
#           print(await request.json())
#       except:
#           print( "no body")
#       response = await call_next(request)
#       return response

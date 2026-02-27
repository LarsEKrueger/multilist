#! /usr/bin/python3

from multilist import db
import multilist.version as mlv
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from pydantic_settings import BaseSettings

import asyncio
from contextlib import asynccontextmanager

class AppSettings( BaseSettings):
    ML_DB_JSON : str = "multilist.json"
    ML_SYNC_URL : str = "localhost:8001"

app_settings = AppSettings()
print(app_settings.ML_DB_JSON)

async def backgroundSync():
    """Function to run in the background. It will periodically connect to other servers and synchronize the databases."""
    while True:
        print("ping")
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(backgroundSync())
    yield


database = db.Database(app_settings.ML_DB_JSON)

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
    return { "name": mlv.name, "version": mlv.version }


@app.get("/lists")
async def getLists():
    return database.getLists()


@app.post("/lists")
async def addList():
    database.addList()
    return {}


class ListProps(BaseModel):
    name: str | None = None
    priority: int | None = None
    warning_period: str | None = None


@app.put("/list/{listId}")
async def updateList(listId: str, listProps: ListProps):
    database.updateList(
        listId, listProps.name, listProps.priority, listProps.warning_period
    )
    return {}


@app.delete("/list/{listId}")
async def deleteList(listId: str):
    try:
        database.deleteList(listId)
    except Exception:
        return False
    return True


def optField(out, d, k):
    if k in d:
        out[k] = d[k]


@app.get("/list/{listId}")
async def listProps(listId: str):
    lp = database.getListProperties(listId)
    res = {}
    optField(res, lp, "name")
    optField(res, lp, "priority")
    optField(res, lp, "warning_period")
    return res


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


class ItemProps(BaseModel):
    subject: str | None = None
    details: str | None = None
    expires: str | None = None
    priority: int | None = None
    status: str | None = None


@app.put("/item/{listId}/{itemId}")
async def updateItem(listId: str, itemId: str, itemProps: ItemProps):
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

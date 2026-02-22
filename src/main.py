#! /usr/bin/python3

from multilist import db
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI()

database = db.Database("test.json")


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

@app.put("/item/{listId}/{itemId}")
async def updateItem(listId: str, itemId:str, itemProps: ItemProps):
    database.updateItem(
        listId, itemId, listProps.name, listProps.priority, listProps.warning_period
    )
    return {}

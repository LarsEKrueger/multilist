#! /usr/bin/python3

from multilist import db
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

database = db.Database( "test.json")

def serveFile(filename):
    # TODO: Use install folder
    with open( filename, "rt") as f:
        s = f.read()
    return HTMLResponse(s)

from starlette.concurrency import iterate_in_threadpool

@app.get("/")
@app.get("/index.html")
async def root():
    return serveFile("html/app.html")

@app.get("/jquery.js")
async def jquery():
    return serveFile("jquery/jquery-4.0.0.min.js")

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

@app.put("/updateList/{listId}")
async def updateList(listId:str, listProps:ListProps):
    print( f'{listId}: {listProps}')
    database.updateList(listId,listProps.name,listProps.priority,listProps.warning_period)
    return {}

def optField(out,d,k):
    if k in d:
        out[k] = d[k]

@app.get("/listProps/{listId}")
async def listProps(listId:str):
    lp = database.getListProperties(listId)
    res = {}
    optField(res,lp,"name")
    optField(res,lp,"priority")
    optField(res,lp,"warning_period")
    return res

@app.get("/items/{listId}")
async def items(listId:str):
    return database.getItems(listId)

@app.get("/item/{listId}/{itemId}")
async def itemProp(listId:str,itemId:str):
    return database.getItemProperties(listId,itemId)

@app.post("/items/{listId}")
async def addItem(listId:str):
    database.addItem(listId)

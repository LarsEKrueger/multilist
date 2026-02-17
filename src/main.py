#! /usr/bin/python3

from multilist import db
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

database = db.Database( "test.json")

@app.get("/")
async def root():
    return HTMLResponse("<html><title>My App</title><body>Lars was here</body></html>")

@app.get("/lists")
async def getLists():
  return database.getLists()

@app.post("/addList")
async def addList():
    database.addList()
    return {}


#! /usr/bin/python3

from multilist import db
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

database = db.Database( "test.json")

def serveFile(filename):
    # TODO: Use install folder
    with open( filename, "rt") as f:
        s = f.read()
    return HTMLResponse(s)

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

@app.post("/addList")
async def addList():
    database.addList()
    return {}


# Manage multiple (TODO) lists on multiple computers with a local-first attitude

## Requirements

* Manage multiple lists
  * Add list
  * Delete an empty list
  * Update list properties
  * List properties
    * name
    * priority
    * warning period
* Manage multiple entries per list
  * Add entry
  * Delete entry
  * Update entry
  * Entry fields
    * Subject
    * Detail Text
    * Expiration DateTime (optional)
    * Priority (optional)
    * Status (optional)
* Store lists persistently
* Synchronize lists with a configurable list of computers whenever they are online

## Non-Use cases / Rejected Requirements
* Authentification for manipulating lists: Teaching example / for local use only
* Authentification for synchronisation: Teaching example / for use in local network only

## Installation

* Install python > 3.10
* Clone the repo
* Run `python3 -m venv venv`
* Run
  * in Linux: `. venv/bin/activate`
  * in Windows: `venv\Scripts\activate.bat`
* Run `pip install -v -r requirements.txt`

## Start

### Environment variables

Set the environment variables (if you want to deviate from the following default values):

    ML_DB_JSON=multilist.json
    ML_SYNC_URL=http://myothercomputer:8000

### Start the server

* Change the directory/folder to where you cloned the repo to.
* Run
  * in Linux: `. venv/bin/activate`
  * in Windows: `venv\Scripts\activate.bat`
* Run `fastapi run src/main.py`
  * Append `--port <number>` if you want to deviate from the default 8000

### Windows Autostart

The following steps are required to execute the server without a command window.

* Create a file e.g. `start.bat` containing the commands above as required.
* Create a file e.g. `start.ps1` containing

    Start-Process <full path to start.bat> -WindowStyle Hidden

* Open the Task Scheduler
* Create a new task (Create simple task) to be run at every login
* Select `powershell.exe` with parameters `-ExecutionPolicy Bypass -File <full path to start.ps1>`
* Mark the task *hidden* on the overview tab

[Source](https://www.ninjaone.com/blog/run-bat-file-in-the-background-using-task-scheduler/)

## Roadmap

### Legend

* ☐ = not done yet
* ✔ = done

### Versions History and Future
* ✔ MVP
  * ✔ Initial design
  * ✔ Simple JSON db
  * ✔ FastAPI
  * ✔ jquery frontend
  * ✔ Basic CSS
  * ✔ adding lists
  * ✔ adding items
* ✔ 0.0: local only
  * ✔ editing fields
  * ✔ deleting items
  * ✔ sort by priority
  * ✔ UUID data base
  * ✔ Show Items that expire soon
* ☐ 0.1: local first
  * ✔ Store last modified time
  * ✔ Synchronisation
  * ✔ Only return public DB fields
* ☐ 0.2: fancy
  * ☐ Frontend design
  * ☐ jquery UI
  * ☐ Datepicker
  * ☐ Duration Picker
  * ☐ Text input via <input> / <textbox>
  * ☐ Update frontend when sync changed something
  * ☐ Error handling in JS/AJAX

## Design decisions
* Item ids must remain stable
* Item ids will be used by front-end for DOM object ids


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

## Design decisions
* Item ids must remain stable
* Item ids will be used by front-end for DOM object ids

## Roadmap

### Legend

* ☐ = not done yet
* ✔ = done

* ✔ MVP
  * ✔ Initial design
  * ✔ Simple JSON db
  * ✔ FastAPI
  * ✔ jquery frontend
  * ✔ Basic CSS
  * ✔ adding lists
  * ✔ adding items
* ☐ 0.1: local only
  * ✔ editing fields
  * ✔ deleting items
  * ✔ sort by priority
  * ✔ UUID data base
  * ✔ Show Items that expire soon
* ☐ 0.2: local first
  * ☐ make thread-safe
  * ☐ Synchronisation
    * ☐ Backend
    * ☐ Update frontend when sync changed something
  * ☐ Only return public DB fields
  * ☐ Error handling in JS/AJAX
* ☐ 0.3: fancy
  * ☐ Frontend design
  * ☐ jquery UI
  * ☐ Datepicker
  * ☐ Duration Picker
  * ☐ Text input via <input> / <textbox>


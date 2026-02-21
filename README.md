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

## Roadmap

### Legend

* ☐ = not done yet
* ✔ = done

* ☐ 0.1: MVP
  * ✔ Initial design
  * ✔ Simple JSON db
  * ✔ FastAPI
  * ✔ jquery frontend
  * ✔ Basic CSS
  * ✔ adding lists
  * ✔ adding items
* ☐ 0.2: local only
  * ☐ editing fields
  * ☐ deleting items
  * ☐ Show Items that expire soon
  * ☐ Logging fails with fallbacks
* ☐ 0.3: local first
  * ☐ git-style data base
  * ☐ make thread-safe
  * ☐ Synchronisation
  * ☐ Only return public DB fields


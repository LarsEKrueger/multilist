from multilist import db

database = db.Database("test.json")

# Add two lists
database.addList()
database.addList()

# Set properties based on the index of the list
for listInd, listId in enumerate(database.getLists()):

    # Add items. This has to be done first because updateList changes the listId.
    for i in range(listInd + 1):
        database.addItem(listId)

    # Set item properties based on index
    for itemInd, itemId in enumerate(database.getItems(listId)):
        database.updateItem(
            listId,
            itemId,
            subject=f"Item {listInd+1} - {itemInd+1}",
            details=f"In List {listInd+1}\nItem {itemInd+1}",
            expires=f"expiration {listInd+1}.{itemInd+1}",
            priority=10 * listInd + itemInd,
            status="none",
        )

    database.updateList(
        listId,
        name=f"List {listInd+1}",
        priority=100 + 10 * listInd,
        warning_period=f"warning {listInd+1}",
    )

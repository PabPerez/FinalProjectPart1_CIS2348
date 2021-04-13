#Pablo Perez
#PSID: 1770045

#More comments will be added soon, I accidentally looked over that step.
import os
import datetime

#sets boolean for the header in case it's included
headerInc = False
def newCSV(content, column, path):
    saveData = []
    if headerInc:
        saveData.append(','.join(column))
    for dataRow in content:
        saveData.append(newRow(column,dataRow))
    with open(path, 'w') as file:
        file.write('\n'.join(saveData))
#Goes through CSV files column by column
def filterCSV(path, cols):
    line = []
    #opens file with read option
    with open(path, 'r') as file:
        lines = file.read().splitlines()
        for x in lines:
            line.append(filterRow(cols, x))
    return line
def newRow(head, content):
    row = []
    for i in head:
        row.append(str(content[i]))
    return ','.join(row)
def filterRow(header, row):
    rowDict = dict()
    #splits each row at the comma
    for i, r in zip(header, row.split(',')):
        rowDict[i] = r.strip()
    return rowDict
def main (mP, pP, sP):
    manufacturer = filterCSV(mP, ["item ID", "manufacturer name", "item type", "damaged indicator"])
    prices = filterCSV(pP, ["item ID", "price"])
    services = filterCSV(sP, ["item ID", "service date"])
    item_list = dict()
    #The following for loops are included so that the manufacturers, prices, and services are added to the new
    #                                                                               transferred list
    for m in manufacturer:
        item_list[m["item ID"]] = m
    for p in prices:
        item_list[p["item ID"]]["price"] = p["price"]
    for s in services:
        item_list[s["item ID"]]["service date"] = s["service date"]
    newCSV(sorted(list(item_list.values()), key=lambda x: x["manufacturer name"]), ["item ID", "manufacturer name",
        "item type", "price", "service date", "damaged indicator"], "FullInventory.csv")
    now = datetime.datetime.now().date()
    pastService = []
    damagedItems = []
    types = dict()
    for item in item_list.values():
        if item["damaged indicator"] != "":
            damagedItems.append(item)
        if item["item type"] not in types:
            types[item["item type"]] = []
        types[item["item type"]].append(item)
        serviceDate = item["service date"].split('/')
        date = datetime.date(int(serviceDate[2]), int(serviceDate[0]), int(serviceDate[1]))
        item["date"] = date
        if date < now:
            pastService.append(item)
    newCSV(sorted(damagedItems, key=lambda x: x["price"], reverse=True), ["item ID", "manufacturer name",
        "item type", "price", "service data", "damaged indicator"], "DamagedInventory.csv")
    for i, items in types.items():
        newCSV(sorted(items, key=lambda x: x["item ID"]), ["item ID", "manufacturer name", "item type", "price",
        "service date", "damaged indicator", ""], "{}Inventory.csv".format(i))
    newCSV(sorted(pastService, key=lambda x: x["date"]), ["item ID", "manufacturer name", "item type", "price",
        "service date"], "PastServiceDateInventory.csv")
if __name__ == '__main__':
    manufacturerFile = "ManufacturerList.csv"
    while not os.path.exists(manufacturerFile):
        manufacturerPath = input('Input absolute path for file: ManufacturerList.csv')
    priceFile = "PriceList.csv"
    while not os.path.exists(priceFile):
        pricePath = input('Input absolute path for file: PriceList.csv')
    serviceFile = "ServiceDatesList.csv"
    while not os.path.exists(serviceFile):
        servicePath = input('Input absolute path for file: ServiceDatesList.csv')
    main(manufacturerFile, priceFile, serviceFile)
#Pablo Perez
#PSID: 1770045

#csv was imported so that the program can read the input csv files and write new ones
#datetime was imported so that we can later figure out which items are past their service date
import csv
from datetime import datetime

# The sorted_inventory class is used to hold methods that make files to hold inventory based on user input
class sorted_inventory:
    def __init__(self, item_list):
        #Must provide list of all items to create new files
        self.item_list = item_list
    def totalInventory(self):
        #Makes a new csv file to input all of the inventory from the FullInventory.csv
        #Opens FullInventory.csv with writing privileges
        with open('FullInventory.csv', 'w') as file:
            items = self.item_list
            #Arranges items in alphabetical order based on manufacturer
            keys = sorted(items.keys(), key=lambda x: items[x]['manufacturer'])
            #The following for loop iterates through each item so that the manufacturers, prices, and services are
            #added to the new csv file
            for item in keys:
                id = item
                manufacturerName = items[item]['manufacturer']
                item_type = items[item]['item_type']
                price = items[item]['price']
                service_day = items[item]['service_day']
                damaged_item = items[item]['damaged_item']
                file.write('{}, {}, {}, {}, {}, {}'.format(id, manufacturerName, item_type, price, service_day,
                                                           damaged_item))
    def damaged_item(self):
        #Makes a csv file for damaged items
        items = self.item_list
        #items are sorted by how expensive they are in descending order due to the reverse=True
        keys = sorted(items.keys(), key=lambda x: items[x]['price'], reverse=True)
        #open damaged_itemInventory.csv with writing privileges in order to add damaged items to new file
        with open('damaged_itemInventory.csv', 'w') as file:
            for item in keys:
                id = item
                manufacturerName = items[item]['manufacturer']
                item_type = items[item]['item_type']
                price = items[item]["price"]
                service_day = items[item]['service_day']
                damaged_item = items[item]['damaged_item']
                #if the item is damaged, add it to the new damaged items csv file that was created at the beginning of
                # the method
                if damaged_item:
                    file.write('{}, {}, {}, {}, {}'.format(id, manufacturerName, item_type, price, service_day))
    def expService(self):
        #Makes a csv file that will be filled with items that are past their service date
        items = self.item_list
        #The following sorts the items by service date from the latest date to the most recent by using reverse=True
        keys = sorted(items.keys(), key=lambda x: datetime.strptime(items[x]['service_day']).date(), reverse=True)
        #open PastServiceDateInventory.csv with writing privileges
        with open('PastServiceDateInventory.csv', 'w') as file:
            for i in keys:
                id = i
                manufacturerName = items[i]['manufacturer']
                item_type = items[i]['item_type']
                price = items[i]['price']
                service_day = items[i]['service_day']
                damaged_item = items[i]['damaged_item']
                current_Day = datetime.now().date()
                service_expiration = datetime.strptime(service_day).date()
                expired = service_expiration < current_Day
                #if the item is expired, add the item's data into the new csv file
                if expired:
                    file.write('{}, {}, {}, {}, {}, {}'.format(id, manufacturerName, item_type, price, service_day,
                                                               damaged_item))
    def type_file(self):
        items = self.item_list
        #new list is made for the different types of items
        item_types = []
        #items are then sorted by their ID
        keys = sorted(items.keys())
        #iterate through the items and add types of items into the new item_types list if they are not already there
        for x in items:
            item_type = items[x]['item_type']
            if item_type not in item_types:
                item_types.append(item_type)
        #iterate through item_types list and give each type their own file
        for y in item_types:
            file_name = y.capitalize() + 'Inventory.csv'
            #open item_type file with writing privileges
            with open(file_name, 'w') as file:
                for item in keys:
                    id = item
                    manufacturerName = items[item]['manufacturer']
                    price = items[item]['price']
                    service_day = items[item]['service_day']
                    damaged_item = items[item]['damaged_item']
                    item_type = items[item]['item_type']
                    #if the item matches the type, add it into the type's file
                    if item == item_type:
                        file.write('{}, {}, {}, {}, {}'.format(id, manufacturerName, price, service_day, damaged_item))
if __name__ == '__main__':
    #items is set to an empty dictionary
    items = {}
    #'files' becomes a list with the following 3 csv files
    files = ['ManufacturerList.csv', 'PriceList.csv', 'ServiceDatesList.csv']
    #iterates through each file
    for file in files:
        #opens first file in read view for csv files
        with open(file, 'r') as csv_file:
            #csv_reader reads the file(s) contents between commas to only get useful data
            csv_reader = csv.reader(csv_file, delimiter=',')
            #iterates through each item in specific file
            for line in csv_reader:
                #item_id is set as the first item in the file being currently read
                item_id = line[0]
                #if the file being read is the same as the ManufacturerList.csv...
                if file == files[0]:
                    #assigns values for item_id, manufacturerName, item_type, and damaged_item based on the order they
                    #were read in the csv_reader
                    items[item_id] = {}
                    manufacturerName = line[1]
                    item_type = line[2]
                    damaged_item = line[3]
                    #.strip() is added to manufacturerName and item_type so that unnecessary leading and trailing
                    #characters are removed
                    items[item_id]['manufacturer'] = manufacturerName.strip()
                    items[item_id]['item_type'] = item_type.strip()
                    items[item_id]['damaged_item'] = damaged_item
                #Or if the file is the same as the PriceList.csv file....
                elif file == files[1]:
                    #assign price the value of the 2nd positioned character/value of the file being read
                    price = line[1]
                    items[item_id]['price'] = price
                #Or if the file being read matches the ServiceDateList.csv
                elif file == files[2]:
                    #assign service day the value of the 2nd positioned character/value of the file being read
                    service_day = line[1]
                    items[item_id]['service_day'] = service_day
    inventory = sorted_inventory(items)
    #the following creates the files used to put sorted/filtered data from the previously defined methods
    inventory.totalInventory()
    inventory.damaged_item()
    inventory.expService()
    inventory.type_file()
    #create a new empty list for types of items and for manufacturers
    item_types = []
    manufacturers = []
    #iterates through manufacturers and item types and makes sure that there are no repeats of either in their
    #respective lists
    #If a manufacturer or type is not in their respective list, they are added
    for x in items:
        Verified_manu = items[x]['manufacturer']
        Verified_type = items[x]['item_type']
        if Verified_manu not in item_types:
            manufacturers.append(Verified_manu)
        if Verified_type not in item_types:
            item_types.append(Verified_type)
        #begins querying user about a specific item or asks if they would like to quit
        query_user = input("Input Manufacturer and Item type or enter 'q' to quit:")
        if query_user == 'q':
            exit
        else:
            #check each word from user to see if there is a match in manufacturer and item type
            user_Man = None
            userType = None
            #manufacturer and item type are split
            query_user = query_user.split()
            #boolean is used to ensure that the input is valid
            bad_input = False
            for word in query_user:
                if word in manufacturers:
                    #if the manufacturer that the user input is already in the manufacturer list, boolean tells program
                    #that the input is not good: hence bad_input = True as opposed to the original False status
                    if user_Man:
                        bad_input = True
                    else:
                    #otherwise, the manufacturer chosen by the user is the chosen manufacturer
                        user_Man = word
                elif word in item_types:
                    # if the item type that the user input is already in the type list, boolean tells program that the
                    # input is not good
                    if userType:
                        bad_input = True
                    else:
                        #otherwise, the type of item chosen by the user is used
                        userType = word
            if not user_Man:
                print("No such item in inventory")
            elif not userType:
                print("No such item in inventory")
            elif bad_input:
                print("No such item in inventory")
            else:
                #Items are sorted in descending order from most to least expensive
                keys = sorted(items.keys(), key=lambda x: items[x]['price'], reverse=True)
                #Creates an empty list for any items that match
                matching_items = []
                #Creates an empty list for items with different manufacturers but with same types
                similar_items = []
                for item in keys:
                    # Expired and damaged items are not included
                    #If the item type matches the item type input by the user...
                    if items[item]['item_type'] == userType:
                        #check that current day isn't past the service expiration date
                        current_Day = datetime.now().date()
                        service_day = items[item]['service_day']
                        service_expiration = datetime.strptime(service_day).date()
                        expired = service_expiration < current_Day
                        #if the manufacturer also matches the input from the user and the inputs aren't expired/damaged
                        if items[item]['manufacturer'] == user_Man:
                            if not expired and not items[item]['damaged_item']:
                                #add the items to the matching items list
                                matching_items.append((item, items[item]))
                        else:
                            #if the manufacturer isn't exact but they are not expired/damaged, add to similar items list
                            if not expired and not items[item]['damaged_item']:
                                similar_items[item] = items[item]
                #If the items match, call on the item variables and print them out for the user
                if matching_items:
                    item = matching_items[0]
                    item_id = item[0]
                    manufacturerName = item[1]['manufacturer']
                    item_type = item[1]['item_type']
                    price = item[1]['price']
                    print("Your item is: {}, {}, {}, {}\n".format(item_id, manufacturerName, item_type, price))
                    #If the items are similar, print out the item that is as close to the price of the matched item
                    if similar_items:
                        matched_price = price
                        #Get the similar item with the closest price to the initial item
                        similarItem = None
                        similarPrice = None
                        for item in similar_items:
                            if similarPrice == None:
                                closes_item = similar_items[item]
                                #gets price difference between the similar item and the item input by the user
                                similarPrice = abs(int(matched_price) - int(similar_items[item]['price']))
                                item_id = item
                                manufacturerName = similar_items[item]['manufacturer']
                                item_type = similar_items[item]['item_type']
                                price = similar_items[item]['price']
                            difference = abs(int(matched_price) - int(similar_items[item]['prices']))
                            #if the difference in price is less than the price of the similar item, assign item and
                            #difference values to the similar item
                            if difference < similarPrice:
                                similarItem = item
                                similarPrice = difference
                                item_id = item
                                manufacturerName = similar_items[item]['manufacturer']
                                item_type = similar_items[item]['item_type']
                                price = similar_items[item]['price']
                                #inform the user about the similar item and show them the info on that item
                                print("You may, also, consider: {}, {}, {}, {}".format(item_id, manufacturerName,
                                                                                       item_type, price))
                else:
                    print("No such item in inventory")
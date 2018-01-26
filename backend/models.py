from inventory.backend.database import read, write


class InvalidKeyword(Exception):
    pass


class InvalidId(Exception):
    pass


class Item:
    name = None
    price = None
    id = None

    def __init__(self, name, price, id=None):
        self.name = name
        self.price = float(price)
        self.id = id

    def save(self, insert=True, update=False):
        """
        Saves / Updates an Item to the database

        :param kwargs: Keyword arguments for deciding whether to save or update this item object
        Keyword arguments:

        update -- Updates the current object with current data
        insert -- Inserts a data into the database with current data

        :return: Number of affected rows
        """
        if update == True:
            if self.id == None:
                raise InvalidId
            result = write(
                "UPDATE items set `name`= '{}',`price`='{}' where id = '{}' ".format(self.name, self.price, self.id))
            return result
        elif insert == True:
            result = write("INSERT into items (`name`,`price`) values('{}','{}')".format(self.name, self.price))
            return result
        else:
            raise InvalidKeyword

    def remove(self):
        """
        Removes an item from the database
        :return:
        """
        write("DELETE FROM `items` WHERE `id`='{}".format(self.id))

    def __str__(self):
        return self.name


class Inventory:
    id = None
    barcode = None
    sold = None
    price = None
    itemid = None

    def __init__(self, barcode, sold, price, itemid, id=None):
        self.id = id
        self.barcode = barcode
        self.sold = sold
        self.price = price
        self.itemid = itemid

    def save(self, insert=True, update=False):
        """
        Saves / Updates an Item to the database

        :param kwargs: Keyword arguments for deciding whether to save or update this item object
        Keyword arguments:

        update -- Updates the current object with current data
        insert -- Inserts a data into the database with current data

        :return: Number of affected rows
        """
        if update == True:
            if self.id == None:
                raise InvalidId
            result = write()
            return result
        elif insert == True:
            result = write("INSERT into items (`name`,`price`) values('{}','{}')".format(self.name, self.price))
            return result
        else:
            raise InvalidKeyword

    def remove(self):
        """
        Removes an item from the database
        :return:
        """
        write("DELETE FROM `items` WHERE `id`='{}".format(self.id))

    def __str__(self):
        return self.name



class InventoryDB:
    def getAllItems(self):
        """
        Gets all the Items from the inventory as Item objects

        :return: List of Item Objects
        """
        items = read('SELECT * FROM items')
        items_ = []
        for i in items:
            anItem = Item(name=i["name"], price=i["price"], id=i["id"])
            items_.append(anItem)
        return items_

    def getItemWithId(self, item):
        """
        Gets Item with a particular id

        :return:
        """
        items = read('SELECT * FROM items where id = \'{}\''.format(item.id))
        items_ = []
        for i in items:
            anItem = Item(name=i["name"], price=i["price"], id=i["id"])
            items_.append(anItem)
        return items_

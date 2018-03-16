from .database import read, write


class InvalidKeyword(Exception):
    pass


class InvalidId(Exception):
    pass


class Item:
    table_name = "items"
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
        write("DELETE FROM `items` WHERE `id`='{}'".format(self.id))

    def __str__(self):
        return self.name


class Inventory:
    table_name = "inventory"
    id = None
    barcode = None
    sold = None
    price = None
    itemname = None
    manufacturer = None
    quantity = None
    category = None

    def __init__(self, barcode, sold, price, itemname, manufacturer, quantity, category, id=None):
        self.id = barcode
        self.barcode = barcode
        self.sold = sold
        self.price = price
        self.itemname = itemname
        self.manufacturer = manufacturer
        self.quantity = quantity
        self.category = category

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
            query = "UPDATE `inventory` set `sold`='{}',`price`='{}',`itemname`='{}',`manufacturer`='{}',`quantity`={}, `category`='{}' where barcode={};".format(
                self.sold, self.price, self.itemname, self.manufacturer,
                self.quantity, self.category, self.barcode)
            print(query)
            result = write(query)
            return result
        elif insert == True:
            result = write(
                "INSERT into {} (`itemname`,`price`,`sold`,`barcode`,`manufacturer`,`quantity`,`category`) values('{}','{}','{}','{}','{}','{}','{}')".format(
                    self.table_name,
                    self.itemname,
                    self.price,
                    self.sold,
                    self.barcode,
                    self.manufacturer,
                    self.quantity,
                    self.category
                ))
            return result
        else:
            raise InvalidKeyword

    def remove(self):
        """
        Removes an item from the database
        :return:
        """
        write("DELETE FROM `items` WHERE `id`='{}'".format(self.id))

    def __str__(self):
        return self.barcode


class Sales:
    id = None
    barcode = None
    time = None
    quantity = None
    itemname = None
    amount = None
    category = None
    invoice_no = None
    customername = None
    paymentmode = None
    tip = None
    cash = None
    card = None

    def __init__(self, barcode, time, quantity, itemname, amount, category, invoice_no, customername, paymentmode,
                 tip, cash, card, id=None):
        self.id = id
        self.barcode = barcode
        self.time = time
        self.quantity = quantity
        self.itemname = itemname
        self.amount = amount
        self.category = category
        self.invoice_no = invoice_no
        self.customername = customername
        self.paymentmode = paymentmode
        self.tip = tip
        self.cash = cash
        self.card = card

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
            query = "UPDATE `sales` set `barcode`='{}',`time`='{}',`quantity`='{}',`itemname`='{}',`amount`='{}'," \
                    "`invoice_no`='{}', `category`='{}', `customername`='{}',`paymentmode`='{}', `tip`='{}', `cash`='{}', `card`='{}', where id={};".format(
                self.barcode, self.time, self.quantity, self.itemname, self.amount, self.invoice_no, self.category,
                self.customername, self.paymentmode,self.tip, self.cash, self.card,
                self.id)
            print(query)
            result = write(query)
            return result
        elif insert == True:
            result = write(
                "INSERT into `sales` (`barcode`,`time`,`quantity`,`itemname`,`amount`,`category`,`invoice_no`,`customername`,`paymentmode`,`tip`,`cash`,`card`) "
                "values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    self.barcode,
                    self.time,
                    self.quantity,
                    self.itemname,
                    self.amount,
                    self.category,
                    self.invoice_no,
                    self.customername,
                    self.paymentmode,
                    self.tip,
                    self.cash,
                    self.card
                ))
            return result
        else:
            raise InvalidKeyword

    def remove(self):
        """
        Removes an item from the database
        :return:
        """
        write("DELETE FROM `items` WHERE `id`='{}'".format(self.id))

    def __str__(self):
        return self.barcode + " " + self.itemname


class Activity:
    def __init__(self, barcode, time, activity, transactiontype, amount):
        self.amount = amount
        self.id = id
        self.activity = activity
        self.transactiontype = transactiontype
        self.item = barcode
        self.time = time

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
            # if self.id == None:
            #     raise InvalidId
            # query = "UPDATE `sales` set `barcode`='{}',`time`='{}',`quantity`='{}',`itemname`='{}',`amount`='{}',`category`='{}' where id={};".format(
            #     self.barcode, self.time, self.quantity, self.itemname, self.amount, self.category,
            #     self.id)
            # print(query)
            # result = write(query)
            # return result
            pass
        elif insert == True:
            result = write(
                "INSERT into `activity` (`item`,`activity`,`transactiontype`,`amount`,`time`) values('{}','{}','{}','{}','{}')".format(
                    self.item,
                    self.activity,
                    self.transactiontype,
                    self.amount,
                    self.time
                ))
            return result
        else:
            raise InvalidKeyword

    def remove(self):
        """
        Removes an item from the database
        :return:
        """
        write("DELETE FROM `activity` WHERE `id`='{}'".format(self.id))

    def __str__(self):
        return self.activity + " " + str(self.id)


import datetime


def log(activity, transactiontype, amount=0, barcode="", time=str(datetime.datetime.now())):
    activity = Activity(barcode=barcode, time=time, activity=activity, transactiontype=transactiontype, amount=amount)
    activity.save(insert=True)


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

    def getInventory(self):
        """
        Gets all the inventory records from database

        :return: Array of Inventory objects
        """
        inventory = read("SELECT * FROM inventory")
        data = []
        for i in inventory:
            anItem = Inventory(barcode=i["barcode"], sold=i["sold"], price=i["price"], itemname=i["itemname"],
                               manufacturer=i["manufacturer"], quantity=i["quantity"],
                               category=i["category"])
            data.append(anItem)
        return data

    def getInventoryRecodeByBarcode(self, barcode):
        """
        Gets a record from invetory according to barcode

        :param barcode: barcode to be searched
        :return: Array of Inventory objects matching barcode
        """
        items = read("SELECT * FROM `inventory` where `barcode` = {};".format(barcode))
        # print(items)
        items_ = []
        for i in items:
            anItem = Inventory(barcode=i["barcode"], sold=i["sold"], price=i["price"], itemname=i["itemname"],
                               manufacturer=i["manufacturer"], quantity=i["quantity"], category=i["category"],
                               )
            items_.append(anItem)
        return items_

    def getAllSales(self):
        """
        Get all sales records

        :return:
        """
        items = read("SELECT * FROM sales where 1")
        items_ = []
        for i in items:
            anItem = Sales(barcode=i["barcode"], time=i["time"], quantity=i["quantity"], itemname=i["itemname"],
                           amount=i["amount"], category=i["category"],
                           id=i["id"], invoice_no=i["invoice_no"], customername=i["customername"],
                           paymentmode=i["paymentmode"],tip=i["tip"], cash=i["cash"], card=i["card"])
            items_.append(anItem)

        return items_

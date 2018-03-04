import pymysql.cursors
from . import config


def write(query):
    """
    This function is for write operation on database such as insert/update/delete

    :param query: INSERT/UPDATE/DELETE Query
    :return: Number of affected Rows
    """
    connection = pymysql.connect(host=config.DB_HOST,
                                 user=config.DB_USER,
                                 password=config.DB_PASSWORD,
                                 db=config.DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    rows = None
    try:

        with connection.cursor() as cursor:
            # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            rows = cursor.execute(query)

        connection.commit()
    finally:
        connection.close()
    return rows


def read(query):
    """
    This function is for read operation on database such as insert/update/delete

    :param query: SELECT Query
    :return:
    """
    connection = pymysql.connect(host=config.DB_HOST,
                                 user=config.DB_USER,
                                 password=config.DB_PASSWORD,
                                 db=config.DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    result = None
    try:
        with connection.cursor() as cursor:
            # Read a single record

            cursor.execute(query)
            result = cursor.fetchall()
    except pymysql.err.ProgrammingError:
        print("Table does not exists")
    finally:
        connection.close()
    return result


def setupDatabase():
    """
    Setting up database for inventory management system
    :return:
    """
    setup_log = {}
    try:
        create_activity_table = "CREATE TABLE `activity` (\
                          `id` int(11) NOT NULL AUTO_INCREMENT,\
                          `activity` varchar(80) NOT NULL,\
                          `transactiontype` varchar(80) NOT NULL,\
                          `item` varchar(80) NOT NULL,\
                          `amount` double NOT NULL,\
                          `time` varchar(50) NOT NULL, \
                          PRIMARY KEY (id) \
                        );"
        setup_log["create_items_table"] = write(create_activity_table)

        create_inventory_table = """CREATE TABLE `inventory` (
                                  `barcode` varchar(30) NOT NULL,
                                  `sold` tinyint(1) NOT NULL,
                                  `price` double NOT NULL,
                                  `itemname` varchar(80) NOT NULL, 
                                  `manufacturer` varchar(50) NOT NULL,
                                  `quantity` int(10) NOT NULL,
                                  `category` varchar(80) NOT NULL,
                                   PRIMARY KEY (barcode)
                                );"""
        setup_log["create_inventory_table"] = write(create_inventory_table)

        create_sales_table = "CREATE TABLE `sales` ( \
                             `id` int(11) NOT NULL AUTO_INCREMENT,\
                             `barcode` varchar(30) NOT NULL,\
                             `amount` double NOT NULL,\
                             `time` varchar(50) NOT NULL, \
                             `quantity` int(10) NOT NULL,\
                             `itemname` varchar(80) NOT NULL,\
                             `category` varchar(80) NOT NULL,\
                             `invoice_no` varchar(30) NOT NULL,\
                             `customername` varchar(80) NOT NULL,\
                             `paymentmode` varchar(20) NOT NULL,\
                              PRIMARY KEY (id)\
                             );"
        print(create_sales_table)
        setup_log["create_sales_table"] = write(create_sales_table)

    except pymysql.err.InternalError:
        print("The Database is already setup")
    return setup_log

# r = write("INSERT into items (`name`,`price`) values('Hair Dryer','25') ")
# r = write("UPDATE items set `name`= 'Shampoo' where id = '1' ")
# r = read("SELECT * FROM items ")
# r = write("DELETE FROM `items` WHERE `id`='2'")
# print(setupDatabase())
# print(r)

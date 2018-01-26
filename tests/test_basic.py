import unittest

from inventory.backend.database import setupDatabase, write, read


class DBSetupTest(unittest.TestCase):
    def test(self):
        self.assertEquals(setupDatabase(), {'create_items_table': 0, 'create_inventory_table': 0})


class DBInsertTest(unittest.TestCase):
    def test(self):
        self.assertEqual(write("INSERT into items (`name`,`price`) values('Hair Dryer','25') "), 1,
                         "DB Insert test passed")


class DBReadTest(unittest.TestCase):
    def test(self):
        self.assertEqual(len(read("SELECT * FROM items ")), 1, "DB read test")


class DBUpdateTest(unittest.TestCase):
    def test(self):
        self.assertEqual(write("UPDATE items set `name`= 'Shampoo' where id = '1' "), 1, "DB update test")


class DBDeleteTest(unittest.TestCase):
    def test(self):
        self.assertEqual(write("DELETE FROM `items` WHERE `id`='1'"), 1, "DB delete test ")



        # r = write("INSERT into items (`name`,`price`) values('Hair Dryer','25') ")
        # r = write("UPDATE items set `name`= 'Shampoo' where id = '1' ")
        # r = read("SELECT * FROM items ")
        # r = write("DELETE FROM `items` WHERE `id`='2'")
        # print(setupDatabase())

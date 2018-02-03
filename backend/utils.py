import smtplib

from .backend import config
from .models import Item,InventoryDB


def send_mail(subject, message):
    server = smtplib.SMTP('mai', 25)
    server.starttls()
    server.login(config.EMAIL, config.MAIL_PASSWORD)
    msg = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}\r\n".format(config.EMAIL, config.EMAIL, subject,
                                                                   message)
    response = server.sendmail("support@epsumlabs.com", [config.EMAIL], msg)
    server.quit()
    return response


def add_item(name, barcodenumber, price):
    i = Item(name=name, barcode=barcodenumber, price=price)
    i.addItem()


def remove_item(barcodenumber):
    item = InventoryDB.getInventoryRecodeByBarcode(barcode=barcodenumber)[0]
    item.remove()


def get_items(barcodenumber):
    return InventoryDB.getInventoryRecodeByBarcode(barcode=barcodenumber)

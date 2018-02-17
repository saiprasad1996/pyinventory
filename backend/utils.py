import smtplib

from backend import config
from backend.models import Item,InventoryDB
import datetime

def send_mail(subject, message):
    server = smtplib.SMTP(config.MAIL_HOST, config.MAIL_PORT)
    server.starttls()
    server.login(config.EMAIL, config.MAIL_PASSWORD)
    msg = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}\r\n".format(config.EMAIL, config.EMAIL, subject,
                                                                   message)
    response = server.sendmail(config.EMAIL, [config.EMAIL], msg)
    server.quit()
    return response


def parseDate(datestr):
    '''
    Parses date string to date object. The date string must in the format of yyyy-mm-dd hh:mm

    :param datestr: Date string in the format  yyyy-mm-dd hh:mm
    :return: Parsed date object
    '''
    return datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M%S")

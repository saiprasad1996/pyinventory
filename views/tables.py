from tkinter import *


class DataLengthMismatch(Exception):
    pass


def createTable(window,dataList):
    """
    Creates table using a Frame and labels

    :param window: Root object
    :param dataList: 2-D List
    :return: Frame Object
    """
    try:
        table = Frame(window)
        length = len(dataList[0])

        sizes = [0] * length

        for record in dataList:

            for p, column in enumerate(record):
                if len(str(column)) > sizes[p]:
                    sizes[p] = len(str(column)) + 3

        for row_n, row_data in enumerate(dataList):
            for i, row in enumerate(row_data):
                Label(table, text=str(row), width=sizes[i], borderwidth=2, relief="groove", justify=LEFT, anchor=W,
                      background="white").grid(column=i, row=row_n + 1, sticky=W)

        return table
    except IndexError:
        raise DataLengthMismatch

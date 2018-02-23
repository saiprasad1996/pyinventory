from backend.utils import messagebox


class DataLengthMismatch(Exception):
    pass


def createTable(window, dataList):
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


def createTableMatPlot(dataList):
    if len(dataList) == 1:

        messagebox("No data", message="No data to show")
        return
    else:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        # hide axes
        fig.patch.set_visible(False)

        ax.axis('off')
        ax.axis('auto')

        # df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))
        # print(df.values)

        print(dataList)

        t = ax.table(cellText=dataList, loc='center')
        t.auto_set_font_size(False)
        t.set_fontsize(8)

        fig.tight_layout()

        plt.show()

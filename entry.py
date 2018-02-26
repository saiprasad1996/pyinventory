# import views.additem
# import views.Reports
# import views.salespage
# import views.add_item
# import views.main_page
# import views.categories_kivy
# import views.reports_kivy
#
# if __name__ == "__main__":
#     # views.salespage.vp_start_gui()
#     # views.additem.vp_start_gui()
#     # views.Reports.vp_start_gui()
#     # views.salespage.SalesPage()
#
#     views.add_item.AddItems(category="shampoo").run()
#     # views.main_page.SalesPage().run()
#     # views.categories_kivy.Categories().run()
#     # views.reports_kivy.Reports().run()
#


import views.add_item
import views.main_page
import views.categories_kivy
import views.reports_kivy
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from backend.utils import messagebox
from kivy.app import App
import views.grid
from backend.database import *
from backend.models import InventoryDB
import datetime


class AddItemScreen(Screen):
    category_ = StringProperty('')

    def __init__(self, **kwargs):
        self.name = "additems"
        super(AddItemScreen, self).__init__()
        # self.category = self.manager
        l = views.add_item.AddItems(category=kwargs["category"], manufacturer=kwargs["manufacturer"],
                                    pre_quantity=kwargs["pre_quantity"])
        l.company.bind(on_press=self.toHome)
        self.add_widget(l)

    def toHome(self, event):
        self.manager.current = "sales"
        self.manager.remove_widget(self)


class CategoryScreen(Screen):
    category = StringProperty('')

    def __init__(self, **kwargs):
        self.name = "categories"
        self.id = "category"
        super(CategoryScreen, self).__init__()
        layout = views.categories_kivy.CategoriesLayout()
        self.add_widget(layout)
        layout.company.bind(on_press=self.to_home)
        layout.button_shampoo.bind(on_press=self.toAddItemShampoo)
        layout.button_cond.bind(on_press=self.toAddItemConditioner)
        layout.button_skin.bind(on_press=self.toAddItemSkincare)
        layout.button_color.bind(on_press=self.toAddItemColor)
        layout.button_Misc.bind(on_press=self.toAddItemMisc)
        layout.button_services.bind(on_press=self.toAddItemServices)

    def to_home(self, event):
        self.manager.current = "sales"

    def toAddItemShampoo(self, event):
        self.manager.add_widget(AddItemScreen(name="additems", category="SHAMPOO", manufacturer="", pre_quantity="1"))
        self.manager.current = "additems"

    def toAddItemConditioner(self, event):
        self.manager.add_widget(
            AddItemScreen(name="additems", category="CONDITIONER", manufacturer="", pre_quantity="1"))
        self.manager.current = "additems"

    def toAddItemSkincare(self, event):
        self.manager.add_widget(AddItemScreen(name="additems", category="SKINCARE", manufacturer="", pre_quantity="1"))
        self.manager.current = "additems"

    def toAddItemColor(self, event):
        self.manager.add_widget(
            AddItemScreen(name="additems", category="HAIR COLOR", manufacturer="", pre_quantity="1"))
        self.manager.current = "additems"

    def toAddItemMisc(self, event):
        self.manager.add_widget(AddItemScreen(name="additems", category="MISC", manufacturer="", pre_quantity="1"))
        self.manager.current = "additems"

    def toAddItemServices(self, event):
        self.manager.add_widget(
            AddItemScreen(name="additems", category="SERVICE", manufacturer="Stylist", pre_quantity="0"))
        self.manager.current = "additems"


class SalesScreen(Screen):
    def __init__(self, **kwargs):
        self.name = "sales"
        super(SalesScreen, self).__init__()
        s = views.main_page.SalesPageLayout()
        self.add_widget(s)
        s.button_add.bind(on_press=self.to_categories)
        s.button_report.bind(on_press=self.to_reports)

    def to_categories(self, event):
        self.manager.current = "categories"

    def to_reports(self, event):
        self.manager.current = "reports"


class ReportScreen(Screen):
    layout = None

    def __init__(self, **kwargs):
        self.name = "reports"
        super(ReportScreen, self).__init__()

        self.layout = views.reports_kivy.ReportsLayout()

        self.add_widget(self.layout)
        self.layout.company.bind(on_press=self.to_home)
        # layout.button_services.bind(on_press=self.toTable)
        self.layout.stock_report.bind(on_press=self.toTable)
        self.layout.sales_report.bind(on_press=self.toReadOnlyTable)
        self.selected_date = self.layout.date_entry.text

    def to_home(self, event):
        self.manager.current = "sales"

    def toTable(self, event):
        data = InventoryDB()
        datalist = data.getInventory()
        items = [["Sl No", "Barcode", "Item Name", "Price", "Manufacturer", "Quantity", "Category"]]
        for i in enumerate(datalist):
            items.append([i[0] + 1, i[1].barcode, i[1].itemname, i[1].price, i[1].manufacturer, i[1].quantity,
                          i[1].category])

        self.manager.add_widget(views.grid.EditableTable(
            dataList=items, title="Stock Details"))
        self.manager.current = "editabletable"

    def toReadOnlyTable(self, event):
        datalist = InventoryDB()
        self.layout.selected_date = self.layout.date_entry.text
        datalist = datalist.getAllSales()

        items = [["ID", "Barcode", "Item Name", "Date", "Quantity", "Selling Amount"]]

        selected_date_o = datetime.datetime.strptime(self.layout.selected_date, "%d/%m/%Y")
        for i in datalist:
            date = datetime.datetime.strptime(str(i.time[:10]), "%Y-%m-%d")
            if selected_date_o == date:
                items.append([i.id, i.barcode, i.itemname, i.time[:11], i.quantity, i.amount])

        if len(items) == 1:
            messagebox(title="Oops", message="No data to show")
        else:
            self.manager.add_widget(views.grid.ReadOnlyTable(dataList=items, title="Sales Details"))
            self.manager.current = "readonlytable"

    def renderTableStock(self, event):
        try:
            # selected_date = self.date_entry.text
            selected_date_o = datetime.datetime.strptime(self.selected_date, "%d/%m/%Y")
            datalist = InventoryDB()

            datalist = datalist.getInventory()
            items = [["Sl No", "Barcode", "Item Name", "Price", "Manufacturer", "Quantity", "Category"]]
            for i in enumerate(datalist):
                items.append([i[0] + 1, i[1].barcode, i[1].itemname, i[1].price, i[1].manufacturer, i[1].quantity,
                              i[1].category])

            # reportstable.renderTable(items)
            # reportstable.renderMatPlot(items)
            self.add_widget(views.grid.EditableTable(
                dataList=items))
        except ValueError:
            messagebox(title="Error", message="Please enter a valid date. \nPlease enter the date in dd/mm/yyyy format")


class InventoryScreens(ScreenManager):
    def __init__(self):
        super(InventoryScreens, self).__init__()

        self.add_widget(SalesScreen(name="sales"))
        self.add_widget(CategoryScreen(name="categories"))
        # self.add_widget(AddItemScreen(name="additems"))
        self.add_widget(ReportScreen(name="reports"))
        # self.add_widget(views.grid.EditableTable(
        #     dataList=[["ID", "Barcode", "Item Name", "Date", "Quantity", "Selling Amount"],
        #               ["1", "123445", "Name", "12/02/2017", "45", "10"],
        #               ]))


class InventoryApp(App):
    def build(self):
        return InventoryScreens()


if __name__ == "__main__":
    InventoryApp().run()

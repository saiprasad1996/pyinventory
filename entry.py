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
from kivy.app import App


class AddItemScreen(Screen):
    category_ = StringProperty('')

    def __init__(self, **kwargs):
        self.name = "additems"
        super(AddItemScreen, self).__init__()
        # self.category = self.manager
        l = views.add_item.AddItems(category=kwargs["category"])
        l.company.bind(on_press=self.toHome)
        self.add_widget(l)

    def toHome(self,event):
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

        self.manager.add_widget(AddItemScreen(name="additems", category="SHAMPOO"))
        self.manager.current = "additems"
    def toAddItemConditioner(self, event):

        self.manager.add_widget(AddItemScreen(name="additems", category="CONDITIONER"))
        self.manager.current = "additems"
    def toAddItemSkincare(self, event):

        self.manager.add_widget(AddItemScreen(name="additems", category="SKINCARE"))
        self.manager.current = "additems"
    def toAddItemColor(self, event):

        self.manager.add_widget(AddItemScreen(name="additems", category="HAIR COLOR"))
        self.manager.current = "additems"
    def toAddItemMisc(self, event):

        self.manager.add_widget(AddItemScreen(name="additems", category="MISC"))
        self.manager.current = "additems"
    def toAddItemServices(self, event):

        self.manager.add_widget(AddItemScreen(name="additems", category="SERVICE"))
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
    def __init__(self, **kwargs):
        self.name = "reports"
        super(ReportScreen, self).__init__()
        layout = views.reports_kivy.ReportsLayout()
        self.add_widget(layout)
        layout.company.bind(on_press=self.to_home)

    def to_home(self, event):
        self.manager.current = "sales"


class InventoryScreens(ScreenManager):
    def __init__(self):
        super(InventoryScreens, self).__init__()

        self.add_widget(SalesScreen(name="sales"))
        self.add_widget(CategoryScreen(name="categories"))
        # self.add_widget(AddItemScreen(name="additems"))
        self.add_widget(ReportScreen(name="reports"))


class InventoryApp(App):
    def build(self):
        return InventoryScreens()


if __name__ == "__main__":
    InventoryApp().run()

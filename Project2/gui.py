"""
GUI classes

- LoginDialog: dialog box for login
- CustomerGUI: main customer interface
- RestaurantGUI: restaurant menu page
- EditorGUI: restaurant editor interface

Written by Wenbin Wu
"""

import math
import shelve
import wx
import wx.lib.intctrl
import wx.lib.mixins.listctrl as listmixins
from restaurant import *


class LoginDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        # ----- username -----
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(self, -1, label='Username:')
        self.username_field = wx.TextCtrl(self)
        username_sizer.Add(username_label, 0, wx.ALL | wx.CENTER, 5)
        username_sizer.Add(self.username_field, 0, wx.ALL, 5)

        # ----- password -----
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(self, -1, label='Password:')
        self.password_field = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        password_sizer.Add(password_label, 0, wx.ALL | wx.CENTER, 5)
        password_sizer.Add(self.password_field, 0, wx.ALL, 5)

        # ----- buttons -----
        button_sizer = wx.StdDialogButtonSizer()
        login_button = wx.Button(self, wx.ID_OK, label='Login')
        login_button.SetDefault()
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(login_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        # ----- main container -----
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(username_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(password_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Fit(self)
        self.SetSizer(main_sizer)
        self.CenterOnParent()


class CustomerGUI(wx.Frame, listmixins.ColumnSorterMixin):
    """customer GUI interface"""
    def __init__(self, parent, title, size=(780, 380)):
        wx.Frame.__init__(
            self, parent, title=title, size=size,
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
            )
        self.CenterOnScreen()
        if wx.Platform == '__WXMAC__':
            self.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Monaco'))
        self.panel = wx.Panel(self)

        self.database = 'restaurants'
        self.user_location = None
        self.itemDataMap = {}

        # ----- search field container -----
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.search_field = wx.SearchCtrl(self.panel, size=(350, -1), style=wx.TE_PROCESS_ENTER)
        self.search_field.ShowCancelButton(True)
        self.search_field.ShowSearchButton(True)
        self.search_field.Bind(wx.EVT_TEXT, self.search_restaurant)
        self.location_label = wx.StaticText(
            self.panel, label='Current Location:  Not Set', size=(200, -1)
            )
        self.set_location_button = wx.Button(self.panel, label='Set Location')
        self.set_location_button.Bind(wx.EVT_BUTTON, self.set_location_button_pressed)
        search_sizer.Add(self.search_field, 0, wx.ALL | wx.CENTER, 5)
        search_sizer.Add(self.location_label, 0 , wx.ALL | wx.EXPAND, 5)
        search_sizer.Add(self.set_location_button, 0, wx.ALL | wx.EXPAND, 5)

        # ----- restaurant list container -----
        self.restaurant_list = wx.ListCtrl(self.panel, size=(780, 250), style=wx.LC_REPORT)
        self.restaurant_list.InsertColumn(0, 'Name', width=200)
        self.restaurant_list.InsertColumn(1, 'Cuisine', width=120)
        self.restaurant_list.InsertColumn(2, 'Address', width=60)
        self.restaurant_list.InsertColumn(3, 'Menus', width=280)
        self.restaurant_list.InsertColumn(4, 'Distance', width=60)
        self.restaurant_list.Bind(wx.EVT_LEFT_DCLICK, self.open_restaurant_page)

        # ----- main container -----
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(search_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(self.restaurant_list, 0, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Fit(self.panel)
        self.panel.SetSizer(self.main_sizer)

        # ----- status bar -----
        self.CreateStatusBar()
        self.SetStatusText('Currently in Customer mode.')

        # ----- wxpython built-in listctrl sorter init -----
        listmixins.ColumnSorterMixin.__init__(self, 5)
        self.load()

    def GetListCtrl(self):
        """method required by wx.lib.mixins.listctrl"""
        return self.restaurant_list

    def load_database(self):
        """load data from database into datamap"""
        self.itemDataMap = {}
        with shelve.open(self.database) as db:
            for restaurant in db.values():
                menu_titles = [menu.title for menu in restaurant.menus]
                menu_titles = ' | '.join(menu_titles)
                for address in restaurant.address:
                    row = [restaurant.name, restaurant.cuisine, address, menu_titles, '']
                    index = len(self.itemDataMap)
                    self.itemDataMap[index] = row
        return None

    def populate_data(self, datamap):
        """populate list box with restaurant data"""
        self.restaurant_list.DeleteAllItems()
        for key, data in datamap.items():
            index = self.restaurant_list.InsertItem(self.restaurant_list.GetItemCount(), data[0])
            self.restaurant_list.SetItem(index, 1, data[1])
            self.restaurant_list.SetItem(index, 2, data[2])
            self.restaurant_list.SetItem(index, 3, data[3])
            self.restaurant_list.SetItem(index, 4, data[4])
            self.restaurant_list.SetItemData(index, key)
        return None

    def load(self):
        """load the chosen database data and populate the restaurant list"""
        self.load_database()
        if self.user_location:
            self.calculate_distances(self.user_location)
        else:
            self.populate_data(self.itemDataMap)
        return None

    def search_restaurant(self, event):
        """filter list of restaurants by search text"""
        filter = self.search_field.GetValue()
        results = {
            index: data for index, data in self.itemDataMap.items() if filter.lower() in data[0].lower()
            }
        self.populate_data(results)
        return None

    def calculate_distances(self, location):
        """
        calculate distance from user location to each restaurant 
        and update the restaurant list
        """
        if not self.restaurant_list.GetItemCount():
            return None
        distances = []
        for index, data in self.itemDataMap.items():
            x1, y1 = location
            x2, y2 = data[2].split(',')
            d = math.sqrt((int(x2) - x1)**2 + (int(y2) - y1)**2)
            d = round(d, 2)
            self.itemDataMap[index][4] = str(d)
            distances.append((d, index))
        _, index = min(distances)
        self.populate_data(self.itemDataMap)
        item = self.restaurant_list.GetItem(index)
        item.SetTextColour(wx.BLUE)
        self.restaurant_list.SetItem(item)
        return None

    def set_location_button_pressed(self, event):
        """let customer set the current location and calculate the distance to each restaurant"""
        dialog = wx.Dialog(self, title='Enter Your Location')
        dialog.CenterOnParent()

        x_sizer = wx.BoxSizer(wx.HORIZONTAL)
        x_label = wx.StaticText(dialog, -1, label='X:')
        x_field = wx.lib.intctrl.IntCtrl(
            dialog, value=None, min=0, max=100, limited=True, allow_none=True
            )
        x_sizer.Add(x_label, 0, wx.ALL | wx.CENTER, 5)
        x_sizer.Add(x_field, 0, wx.ALL, 5)

        y_sizer = wx.BoxSizer(wx.HORIZONTAL)
        y_label = wx.StaticText(dialog, -1, label='Y:')
        y_field = wx.lib.intctrl.IntCtrl(
            dialog, value=None, min=0, max=100, limited=True, allow_none=True
            )
        y_sizer.Add(y_label, 0, wx.ALL | wx.CENTER, 5)
        y_sizer.Add(y_field, 0, wx.ALL, 5)

        button_sizer = wx.StdDialogButtonSizer()
        set_button = wx.Button(dialog, wx.ID_OK)
        set_button.SetDefault()
        cancel_button = wx.Button(dialog, wx.ID_CANCEL)
        button_sizer.AddButton(set_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(x_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(y_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Fit(dialog)
        dialog.SetSizer(main_sizer)

        if dialog.ShowModal() == wx.ID_OK:
            x = x_field.GetValue()
            y = y_field.GetValue()
            if not x or not y:
                return None
            self.location_label.SetLabelText(f'Current Location:  {x}, {y}')
            self.user_location = (x, y)
            self.calculate_distances(self.user_location)
        return None

    def open_restaurant_page(self, event):
        """open the menu page for the restaurant"""
        index = self.restaurant_list.GetFirstSelected()
        restaurant = self.restaurant_list.GetItem(index).GetText()
        dialog = RestaurantGUI(self, restaurant, self.database)
        dialog.CenterOnParent()
        dialog.ShowWindowModal()
        return None

    def add_restaurant(self, event):
        """display the editor GUI to add a new restaurant"""
        add_dialog = EditorGUI(
            self, self.database, datamap=self.itemDataMap, title='Add Restaurant'
            )
        add_dialog.CenterOnParent()
        add_dialog.ShowWindowModal()
        return None

    def edit_restaurant(self, event):
        """display the editor GUI to edit a selected restaurant"""
        index = self.restaurant_list.GetFirstSelected()
        if index == -1:
            return None
        restaurant = self.restaurant_list.GetItem(index).GetText()
        edit_dialog = EditorGUI(
            self, self.database, restaurant, datamap=self.itemDataMap, title='Edit Restaurant'
            )
        edit_dialog.CenterOnParent()
        edit_dialog.ShowWindowModal()
        return None

    def delete_restaurant(self, event):
        """delete the selected restaurant"""
        index = self.restaurant_list.GetFirstSelected()
        if index == -1:
            return None
        selected_name = self.restaurant_list.GetItem(index, 0).GetText()
        selected_address = self.restaurant_list.GetItem(index, 2).GetText()
        with shelve.open(self.database) as db:
            for restaurant in db.values():
                if selected_address in restaurant.address:
                    if restaurant.isfranchise:
                        restaurant.address.remove(selected_address)
                        db[selected_name] = restaurant
                    else:
                        del db[selected_name]
        self.restaurant_list.DeleteItem(index)
        self.load()
        return None

    def reload_database(self, event):
        """reload database and update the restaurant list"""
        self.load()
        return None

    def admin_logout(self, event):
        """logout of admin account and disable the admin functions"""
        self.SetTitle('Restaurants Customer GUI')
        self.SetStatusText('Successfully logged out. Currently in customer mode.')

        # ----- disable and remove the admin functions -----
        self.main_sizer.Hide(self.admin_sizer)
        self.main_sizer.Remove(self.admin_sizer)
        self.panel.Layout()
        self.SetSize((780, 380))
        return None

    def admin_login(self):
        """enable the admin functions"""
        self.SetTitle('Restaurants Administrator GUI')
        self.SetStatusText('Successfully logged in. Administrator functions enabled.')

        # ----- unlock and display the admin functions -----
        self.admin_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel, label='Administrator Funcitons')
        add_button = wx.Button(self.panel, wx.ID_ADD)
        add_button.Bind(wx.EVT_BUTTON, self.add_restaurant)
        edit_button = wx.Button(self.panel, wx.ID_EDIT)
        edit_button.Bind(wx.EVT_BUTTON, self.edit_restaurant)
        delete_button = wx.Button(self.panel, wx.ID_DELETE)
        delete_button.Bind(wx.EVT_BUTTON, self.delete_restaurant)
        refresh_button = wx.Button(self.panel, wx.ID_REFRESH)
        refresh_button.Bind(wx.EVT_BUTTON, self.reload_database)
        logout_button = wx.Button(self.panel, label='Logout')
        logout_button.Bind(wx.EVT_BUTTON, self.admin_logout)
        self.admin_sizer.Add(add_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.admin_sizer.Add(edit_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.admin_sizer.Add(delete_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.admin_sizer.Add(refresh_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.admin_sizer.Add(logout_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.main_sizer.Add(self.admin_sizer, 0, wx.ALL | wx.CENTER, 5)
        self.panel.Layout()
        self.SetSize((780, 460))
        return None


class RestaurantGUI(wx.Dialog):
    def __init__(self, parent, restaurant, database=None):
        wx.Dialog.__init__(self, parent=parent)
        if wx.Platform == '__WXMSW__':
            self.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Courier New'))
        elif wx.Platform == '__WXMAC__':
            self.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Monaco'))
        if database:
            with shelve.open(database) as db:
                restaurant = db[restaurant]
        self.SetTitle('Restaurant Page')

        # ----- restaurant info container -----
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        name_label = wx.StaticText(self, label=restaurant.name, style=wx.ALIGN_CENTER)

        # ----- opening hours container -----
        hours_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Business Hours\t(Open / Close)')
        word = iter([
            'Monday:    ', 'Tuesday:   ', 'Wednesday: ', 'Thursday:  ',
            'Friday:    ', 'Saturday:  ', 'Sunday:    '
            ])
        for day, hours in restaurant.hours.items():
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            label = next(word)
            day_label = wx.StaticText(self, label=label)
            opening = wx.StaticText(self, label=hours[0])
            closing = wx.StaticText(self, label=hours[1])
            sizer.Add(day_label, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(opening, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(closing, 0, wx.ALL | wx.EXPAND, 5)
            hours_sizer.Add(sizer)
        left_sizer.Add(name_label, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(hours_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # ----- separator -----
        vline = wx.StaticLine(self, -1, size=(1, -1), style=wx.LI_VERTICAL)

        # ----- menus container -----
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        for menu in restaurant.menus:
            menu_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=menu.title)
            for item, price in menu.items.items():
                item_sizer = wx.BoxSizer(wx.HORIZONTAL)
                name_label = wx.StaticText(self, label=item, size=(300, -1))
                name_label.SetBackgroundColour('#FFF5EE')
                prices_label = wx.StaticText(self, label=price, style=wx.ALIGN_LEFT)
                prices_label.SetBackgroundColour('#E6E6FA')
                item_sizer.Add(name_label, 0, wx.ALL | wx.EXPAND)
                item_sizer.Add(prices_label, 0, wx.ALL | wx.EXPAND)
                menu_sizer.Add(item_sizer, 0, wx.ALL, 2)
            right_sizer.Add(menu_sizer, 0, wx.ALL | wx.EXPAND, 5)
        close_button = wx.Button(self, wx.ID_OK, label='Close')
        right_sizer.Add(close_button, 0, wx.ALL | wx.ALIGN_RIGHT, 10)

        # ----- main container -----
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_sizer)
        main_sizer.Add(vline, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(right_sizer, 0, wx.ALIGN_CENTER, 5)
        main_sizer.Fit(self)
        self.SetSizer(main_sizer)


class EditorGUI(wx.Dialog):
    def __init__(self, parent, database, restaurant=None, datamap=None, title='', size=(760, 450)):
        wx.Dialog.__init__(
            self, parent, title=title, size=size,
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
            )
        if wx.Platform == '__WXMSW__':
            self.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Courier New'))
        elif wx.Platform == '__WXMAC__':
            self.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Monaco'))
        self.restaurant = restaurant
        self.database = database
        self.occupied_addresses = {i[2] for i in datamap.values()}
        self.temp_menus = []  # list of Menu objects

        # ----- restaurant name container -----
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(self, 0, label='Restaurant Name:')
        self.name_field = wx.TextCtrl(self, 0, size=(200, -1))
        name_sizer.Add(name_label, 0, wx.ALL | wx.EXPAND, 5)
        name_sizer.Add(self.name_field, 0, wx.ALL | wx.EXPAND, 5)

        # ----- cuisine type container -----
        cuisine_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cuisine_label = wx.StaticText(self, 0, label='Cuisine:')
        self.cuisine_field = wx.TextCtrl(self, 0, size=(265, -1))
        cuisine_sizer.Add(cuisine_label, 0, wx.ALL | wx.EXPAND, 5)
        cuisine_sizer.Add(self.cuisine_field, 0, wx.ALL | wx.EXPAND, 5)

        # ----- franchise choice container -----
        franchise_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.franchise_label = wx.StaticText(self, 0, label='Franchise:')
        self.is_franchise = wx.Choice(self, -1, (20, -1), choices = ['No', 'Yes'])
        self.is_franchise.Bind(wx.EVT_CHOICE, self.clear_addresses)
        franchise_sizer.Add(self.franchise_label, 0, wx.ALL | wx.EXPAND, 5)
        franchise_sizer.Add(self.is_franchise, 0, wx.ALL | wx.EXPAND, 5)

        # ----- address container ------
        address_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Address')
        xy_sizer = wx.BoxSizer(wx.HORIZONTAL)
        x_label = wx.StaticText(self, -1, label='X:')
        self.x_field = wx.lib.intctrl.IntCtrl(
            self, value=None, min=0, max=100, limited=True, allow_none=True, size=(70, -1)
            )
        y_label = wx.StaticText(self, -1, label='Y:')
        self.y_field = wx.lib.intctrl.IntCtrl(
            self, value=None, min=0, max=100, limited=True, allow_none=True, size=(70, -1)
            )
        add_button = wx.Button(self, label='Add')
        add_button.Bind(wx.EVT_BUTTON, self.add_button_pressed)
        xy_sizer.Add(x_label, 0, wx.ALL | wx.CENTER, 5)
        xy_sizer.Add(self.x_field, 0, wx.ALL, 5)
        xy_sizer.Add(y_label, 0, wx.ALL | wx.CENTER, 5)
        xy_sizer.Add(self.y_field, 0, wx.ALL, 5)
        xy_sizer.Add(add_button, 0, wx.ALL | wx.EXPAND, 5)
        choices_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.entered_addresses = wx.Choice(self, -1, size=(207, -1), choices=[])
        remove_button = wx.Button(self, label='Remove')
        remove_button.Bind(wx.EVT_BUTTON, self.remove_button_pressed)
        choices_sizer.Add(self.entered_addresses, 0, wx.ALL | wx.EXPAND, 5)
        choices_sizer.Add(remove_button, 0, wx.ALL | wx.EXPAND, 5)
        address_sizer.Add(xy_sizer, 0, wx.ALL | wx.EXPAND)
        address_sizer.Add(choices_sizer, 0, wx.ALL | wx.EXPAND)

        # ----- opening hours container -----
        hours_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Business Hours\t(Open / Close)')
        monday_sizer = wx.BoxSizer(wx.HORIZONTAL)
        monday_label = wx.StaticText(self, label='Monday:    ')
        self.monday_opening_field = wx.TextCtrl(self, 0, size=(100, -1))
        self.monday_closing_field = wx.TextCtrl(self, 0, size=(100, -1))
        monday_sizer.Add(monday_label, 0, wx.ALL | wx.EXPAND, 5)
        monday_sizer.Add(self.monday_opening_field, 0, wx.ALL | wx.EXPAND, 5)
        monday_sizer.Add(self.monday_closing_field, 0, wx.ALL | wx.EXPAND, 5)
        tuesday_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tuesday_label = wx.StaticText(self, label='Tuesday:   ')
        self.tuesday_opening_field = wx.TextCtrl(self, 0, size=(100, -1))
        self.tuesday_closing_field = wx.TextCtrl(self, 0, size=(100, -1))
        tuesday_sizer.Add(tuesday_label, 0, wx.ALL | wx.EXPAND, 5)
        tuesday_sizer.Add(self.tuesday_opening_field, 0, wx.ALL | wx.EXPAND, 5)
        tuesday_sizer.Add(self.tuesday_closing_field, 0, wx.ALL | wx.EXPAND, 5)
        wednesday_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wednesday_label = wx.StaticText(self, label='Wednesday: ')
        self.wednesday_opening_field = wx.TextCtrl(self, 0, size=(100, -1))
        self.wednesday_closing_field = wx.TextCtrl(self, 0, size=(100, -1))
        wednesday_sizer.Add(wednesday_label, 0, wx.ALL | wx.EXPAND, 5)
        wednesday_sizer.Add(self.wednesday_opening_field, 0, wx.ALL | wx.EXPAND, 5)
        wednesday_sizer.Add(self.wednesday_closing_field, 0, wx.ALL | wx.EXPAND, 5)
        thursday_sizer = wx.BoxSizer(wx.HORIZONTAL)
        thursday_label = wx.StaticText(self, label='Thursday:  ')
        self.thursday_opening_field = wx.TextCtrl(self, 0, size=(100, -1))
        self.thursday_closing_field = wx.TextCtrl(self, 0, size=(100, -1))
        thursday_sizer.Add(thursday_label, 0, wx.ALL | wx.EXPAND, 5)
        thursday_sizer.Add(self.thursday_opening_field, 0, wx.ALL | wx.EXPAND, 5)
        thursday_sizer.Add(self.thursday_closing_field, 0, wx.ALL | wx.EXPAND, 5)
        friday_sizer = wx.BoxSizer(wx.HORIZONTAL)
        friday_label = wx.StaticText(self, label='Friday:    ')
        self.friday_opening_field = wx.TextCtrl(self, 0, size=(100, -1))
        self.friday_closing_field = wx.TextCtrl(self, 0, size=(100, -1))
        friday_sizer.Add(friday_label, 0, wx.ALL | wx.EXPAND, 5)
        friday_sizer.Add(self.friday_opening_field, 0, wx.ALL | wx.EXPAND, 5)
        friday_sizer.Add(self.friday_closing_field, 0, wx.ALL | wx.EXPAND, 5)
        saturday_sizer = wx.BoxSizer(wx.HORIZONTAL)
        saturday_label = wx.StaticText(self, label='Saturday:  ')
        self.saturday_opening_field = wx.TextCtrl(self, 0, size=(100, -1))
        self.saturday_closing_field = wx.TextCtrl(self, 0, size=(100, -1))
        saturday_sizer.Add(saturday_label, 0, wx.ALL | wx.EXPAND, 5)
        saturday_sizer.Add(self.saturday_opening_field, 0, wx.ALL | wx.EXPAND, 5)
        saturday_sizer.Add(self.saturday_closing_field, 0, wx.ALL | wx.EXPAND, 5)
        sunday_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sunday_label = wx.StaticText(self, label='Sunday:    ')
        self.sunday_opening_field = wx.TextCtrl(self, 0, size=(100, -1))
        self.sunday_closing_field = wx.TextCtrl(self, 0, size=(100, -1))
        sunday_sizer.Add(sunday_label, 0, wx.ALL | wx.EXPAND, 5)
        sunday_sizer.Add(self.sunday_opening_field, 0, wx.ALL | wx.EXPAND, 5)
        sunday_sizer.Add(self.sunday_closing_field, 0, wx.ALL | wx.EXPAND, 5)
        hours_sizer.Add(monday_sizer)
        hours_sizer.Add(tuesday_sizer)
        hours_sizer.Add(wednesday_sizer)
        hours_sizer.Add(thursday_sizer)
        hours_sizer.Add(friday_sizer)
        hours_sizer.Add(saturday_sizer)
        hours_sizer.Add(sunday_sizer)

        # ----- menu item container -----
        menus_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Menus')
        item_sizer = wx.BoxSizer(wx.HORIZONTAL)
        item_label = wx.StaticText(self, 0, label='Item Name: ')
        self.item_field = wx.TextCtrl(self, 0, size=(250, -1))
        price_label = wx.StaticText(self, 0, label='Item Prices:')
        self.price_field = wx.TextCtrl(self, 0, size=(250, -1))
        item_sizer.Add(item_label, 0, wx.ALL | wx.EXPAND, 5)
        item_sizer.Add(self.item_field, 0, wx.ALL | wx.EXPAND, 5)
        item_sizer.Add(price_label, 0, wx.ALL | wx.EXPAND, 5)
        item_sizer.Add(self.price_field, 0, wx.ALL | wx.EXPAND, 5)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.insert_item_button = wx.Button(self, wx.ID_OK, label='Insert Item')
        self.insert_item_button.Bind(wx.EVT_BUTTON, self.insert_item_button_pressed)
        self.modify_item_button = wx.Button(self, wx.ID_OK, label='Modify Item')
        self.modify_item_button.Bind(wx.EVT_BUTTON, self.modify_item_button_pressed)
        self.modify_item_button.Disable()
        self.remove_item_button = wx.Button(self, wx.ID_OK, label='Remove Item')
        self.remove_item_button.Bind(wx.EVT_BUTTON, self.remove_item_button_pressed)
        self.remove_item_button.Disable()
        buttons_sizer.Add(self.insert_item_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        buttons_sizer.Add(self.modify_item_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        buttons_sizer.Add(self.remove_item_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        # ----- menu items list container -----
        self.item_list = wx.ListCtrl(self, size=(700, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.item_list.InsertColumn(0, 'Menu Item', width=350)
        self.item_list.InsertColumn(1, 'Prices', width=300)
        self.item_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.populate_item_fields)
        self.item_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.change_item_buttons)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_label = wx.StaticText(self, 0, label='Menu Title:')
        self.title_field = wx.TextCtrl(self, 0, size=(290, -1))
        self.insert_menu_button = wx.Button(self, wx.ID_OK, label='Insert Menu')
        self.insert_menu_button.Bind(wx.EVT_BUTTON, self.insert_menu_button_pressed)
        self.save_menu_button = wx.Button(self, wx.ID_OK, label='Save Menu')
        self.save_menu_button.Bind(wx.EVT_BUTTON, self.save_menu_button_pressed)
        self.save_menu_button.Disable()
        self.remove_menu_button = wx.Button(self, wx.ID_OK, label='Remove Menu')
        self.remove_menu_button.Bind(wx.EVT_BUTTON, self.remove_menu_button_pressed)
        self.remove_menu_button.Disable()
        title_sizer.Add(title_label, 0, wx.ALL | wx.EXPAND, 5)
        title_sizer.Add(self.title_field, 0, wx.ALL | wx.EXPAND, 5)
        title_sizer.Add(self.insert_menu_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        title_sizer.Add(self.save_menu_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        title_sizer.Add(self.remove_menu_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        # ----- menus list container -----
        self.menu_list = wx.ListCtrl(self, size=(-1, 140), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.menu_list.InsertColumn(0, 'Menu Title', width=350)
        self.menu_list.InsertColumn(1, '# of Items', width=300)
        self.menu_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.populate_menu_items)
        self.menu_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.change_menu_buttons)

        line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)

        # ----- save butttons container -----
        buttons_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        preview_button = wx.Button(self, wx.ID_OK, label='Preview')
        preview_button.Bind(wx.EVT_BUTTON, self.preview_button_pressed)
        save_button = wx.Button(self, wx.ID_OK, label='Save')
        save_button.Bind(wx.EVT_BUTTON, self.save_button_pressed)
        clear_button = wx.Button(self, wx.ID_CLEAR, label='Clear')
        clear_button.Bind(wx.EVT_BUTTON, self.clear_button_pressed)
        cancel_button = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_button_pressed)
        buttons_sizer3.Add(preview_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        buttons_sizer3.Add(save_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        buttons_sizer3.Add(clear_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        buttons_sizer3.Add(cancel_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        menus_sizer.Add(item_sizer, 0, wx.ALL | wx.EXPAND)
        menus_sizer.Add(buttons_sizer, 0, wx.ALL | wx.ALIGN_RIGHT)
        menus_sizer.Add(self.item_list, 0, wx.ALL | wx.EXPAND, 1)
        menus_sizer.Add(title_sizer, 0, wx.ALL | wx. ALIGN_LEFT)
        menus_sizer.Add(self.menu_list, 0, wx.ALL | wx.EXPAND, 1)

        # ----- left container -----
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(name_sizer, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(cuisine_sizer, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(franchise_sizer, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(address_sizer, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(hours_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # ----- right container -----
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(menus_sizer, 0, wx.ALL | wx.EXPAND)
        right_sizer.Add(line, 0, wx.GROW | wx.CENTER | wx.TOP, 5)
        right_sizer.Add(buttons_sizer3, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        # ----- main container -----
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(right_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Fit(self)
        self.SetSizer(main_sizer)

        # when editing an existing restaurant
        # details are pulled to populate the text fields
        if self.restaurant:
            self.populate_form()


    def clear_addresses(self, event):
        """
        remove all addresses entered if there are more than one entered
        and franchise is set to no
        """
        if event.GetString() == 'No' and self.entered_addresses.GetCount() > 1:
            self.entered_addresses.SetItems([])
        return None

    def add_button_pressed(self, event):
        """add a x,y address to the address list"""
        if self.is_franchise.GetCurrentSelection() or not self.entered_addresses.GetCount():
            x = self.x_field.GetValue()
            y = self.y_field.GetValue()
            if x is None or y is None:
                return None
            new_address = f'{x}, {y}'
            address_is_occupied = self.occupied_addresses.intersection([new_address])
            if address_is_occupied:
                self.show_error_message(
                    f'Can not use address {new_address} for this restaurant. Already occupied.'
                    )
                return None
            self.entered_addresses.Append(new_address)
            self.occupied_addresses.add(new_address)
            self.x_field.Clear()
            self.y_field.Clear()
        return None

    def remove_button_pressed(self, event):
        """remove the selected address from the address list"""
        if self.entered_addresses.GetCount():
            selected = self.entered_addresses.GetCurrentSelection()
            address = self.entered_addresses.GetString(selected)
            self.occupied_addresses.discard(address)
            self.entered_addresses.Delete(selected)
        return None

    def insert_item_button_pressed(self, event):
        """insert a new menu item into the items list"""
        item = self.item_field.GetValue()
        price = self.price_field.GetValue()
        if item == '' or price == '':
            return None
        for i in range(self.item_list.GetItemCount()):
            if self.item_list.GetItem(i).GetText() == item:
                dialog = wx.Dialog(self)
                dialog.CenterOnParent()
                sizer = wx.BoxSizer(wx.VERTICAL)
                label = wx.StaticText(dialog, 0, label=f'Item {item} already exist, replace it?')
                button_sizer = wx.BoxSizer(wx.HORIZONTAL)
                yes_button = wx.Button(dialog, wx.ID_OK, label='Yes')
                no_button = wx.Button(dialog, wx.ID_CANCEL, label='No')
                button_sizer.Add(yes_button, 0, wx.ALL | wx.EXPAND, 5)
                button_sizer.Add(no_button, 0, wx.ALL | wx.EXPAND, 5)
                sizer.Add(label, 0, wx.ALL | wx.EXPAND, 5)
                sizer.Add(button_sizer, 0, wx.ALL | wx.EXPAND, 5)
                sizer.Fit(dialog)
                dialog.SetSizer(sizer)
                if dialog.ShowModal() == wx.ID_OK:
                    self.item_list.SetItem(i, 0, item)
                    self.item_list.SetItem(i, 1, price)
                    return None
        self.item_list.Append((item, price))
        self.change_item_buttons(wx.EVT_LIST_ITEM_DESELECTED)
        return None

    def modify_item_button_pressed(self, event):
        """modify the selected menu item"""
        index = self.item_list.GetFirstSelected()
        item = self.item_field.GetValue()
        price = self.price_field.GetValue()
        if item == '' or price == '':
            return None
        self.item_list.SetItem(index, 0, item)
        self.item_list.SetItem(index, 1, price)
        self.item_list.SetItemState(index, 0, wx.LIST_STATE_SELECTED)
        self.change_item_buttons(wx.EVT_LIST_ITEM_DESELECTED)
        return None

    def remove_item_button_pressed(self, event):
        """remove the selected menu item from the items list"""
        if self.item_list.GetItemCount():
            index = self.item_list.GetFirstSelected()
            self.item_list.DeleteItem(index)
        self.change_item_buttons(wx.EVT_LIST_ITEM_DESELECTED)
        return None

    def insert_menu_button_pressed(self, event):
        """insert a new menu into the menus list"""
        title = self.title_field.GetValue()
        num_items = self.item_list.GetItemCount()
        if not title or not num_items:
            self.show_error_message('Error. Can not add an menu with no title or no items.')
            return None
        else:
            self.menu_list.Append((title, str(num_items)))
        new_menu = Menu(self.title_field.GetValue(), {})
        for i in range(num_items):
            name = self.item_list.GetItem(i, 0).GetText()
            price = self.item_list.GetItem(i, 1).GetText()
            new_menu.add_item(name, price)
        self.temp_menus.append(new_menu)
        self.change_menu_buttons(wx.EVT_LIST_ITEM_DESELECTED)
        return None

    def save_menu_button_pressed(self, event):
        """save a modified menu to the menus list"""
        index = self.menu_list.GetFirstSelected()
        title = self.title_field.GetValue()
        num_items = self.item_list.GetItemCount()
        if title == '' or not num_items:
            self.show_error_message('Error. A menu must a title and at least 1 item.')
            return None
        else:
            self.menu_list.SetItem(index, 0, title)
            self.menu_list.SetItem(index, 1, str(num_items))
        modified_menu = Menu(self.title_field.GetValue(), {})
        for i in range(num_items):
            name = self.item_list.GetItem(i, 0).GetText()
            price = self.item_list.GetItem(i, 1).GetText()
            modified_menu.add_item(name, price)
        self.temp_menus[index] = modified_menu
        self.change_menu_buttons(wx.EVT_LIST_ITEM_DESELECTED)
        return None

    def remove_menu_button_pressed(self, event):
        """remove the selected menu from the menus list"""
        index = self.menu_list.GetFirstSelected()
        if not index == -1:
            self.title_field.Clear()
            self.item_list.DeleteAllItems()
            self.menu_list.DeleteItem(index)
            self.temp_menus.pop(index)
        self.change_menu_buttons(wx.EVT_LIST_ITEM_DESELECTED)
        return None

    def preview_button_pressed(self, event):
        """preview restaurant info"""
        restaurant = self.create_restaurant()
        dialog = RestaurantGUI(self, restaurant)
        dialog.SetTitle('New Restaurant Preview')
        dialog.CenterOnParent()
        dialog.ShowModal()
        return None

    def save_button_pressed(self, event):
        """save the restaurant data to the database"""
        restaurant = self.create_restaurant()
        if not restaurant.name or not restaurant.cuisine or not restaurant.address:
            self.show_error_message(
                'Error. Can not save restaurant with no name, cuisine type or an address.'
                )
            return None
        good_hours = True  # assume the hours is entered correctly
        for val in restaurant.hours.values():  # check for bad hours for each day of the week
            if ('' in val) and (not val[0].lower() == 'closed' and not val[1].lower() == 'closed'):
                # bad : either opening or closing is blank
                # bad: neither opening or closing is 'closed'
                # good: otherwise both opening and closing contain non-empty string
                good_hours = False
                break
        if not good_hours:
            self.show_error_message('Error. Can not save restuarant with invalid business hours.')
            return None
        if not restaurant.menus:
            self.show_error_message('Error. Can not save restaurant with no menu.')
            return None
        with shelve.open(self.database) as db:
            if self.restaurant:
                # in the case of editing and exisiting restaurant and the restaurant name is changed
                # delete the original and save the edited version
                del db[self.restaurant]
            db[restaurant.name] = restaurant
        self.Destroy()
        return None

    def clear_button_pressed(self, event):
        """clear all ediable data"""
        self.name_field.Clear()
        self.cuisine_field.Clear()
        self.x_field.Clear()
        self.y_field.Clear()
        self.entered_addresses.Clear()
        self.monday_opening_field.Clear()
        self.monday_closing_field.Clear()
        self.tuesday_opening_field.Clear()
        self.tuesday_closing_field.Clear()
        self.wednesday_opening_field.Clear()
        self.wednesday_closing_field.Clear()
        self.thursday_opening_field.Clear()
        self.thursday_closing_field.Clear()
        self.friday_opening_field.Clear()
        self.friday_closing_field.Clear()
        self.saturday_opening_field.Clear()
        self.saturday_closing_field.Clear()
        self.sunday_opening_field.Clear()
        self.sunday_closing_field.Clear()
        self.title_field.Clear()
        self.item_field.Clear()
        self.price_field.Clear()
        self.item_list.DeleteAllItems()
        self.menu_list.DeleteAllItems()
        self.temp_menus.clear()
        self.change_item_buttons(wx.EVT_LIST_ITEM_DESELECTED)
        self.change_menu_buttons(wx.EVT_LIST_ITEM_DESELECTED)
        return None

    def cancel_button_pressed(self, event):
        """close the editor"""
        self.Destroy()
        return None

    def populate_menu_items(self, event):
        """populate the items list with items from the selected menu"""
        self.item_field.Clear()
        self.price_field.Clear()
        self.item_list.DeleteAllItems()
        menu = self.temp_menus[event.Index]
        for item, price in menu.items.items():
            self.item_list.Append((item, price))
        self.title_field.SetValue(event.GetText())
        self.insert_menu_button.Disable()
        self.save_menu_button.Enable()
        self.remove_menu_button.Enable()
        return None

    def populate_item_fields(self, event):
        """populate item and price fields with the selected item"""
        index = self.item_list.GetFirstSelected()
        name = self.item_list.GetItem(index, 0).GetText()
        price = self.item_list.GetItem(index, 1).GetText()
        self.item_field.SetValue(name)
        self.price_field.SetValue(price)
        self.insert_item_button.Disable()
        self.modify_item_button.Enable()
        self.remove_item_button.Enable()
        return None

    def change_item_buttons(self, event):
        """enable the insert button"""
        self.insert_item_button.Enable()
        self.modify_item_button.Disable()
        self.remove_item_button.Disable()
        self.item_field.Clear()
        self.price_field.Clear()
        return None

    def change_menu_buttons(self, event):
        """enable the insert menu button"""
        self.insert_menu_button.Enable()
        self.save_menu_button.Disable()
        self.remove_menu_button.Disable()
        self.item_list.DeleteAllItems()
        self.title_field.Clear()
        self.item_field.Clear()
        self.price_field.Clear()
        return None

    def show_error_message(self, message):
        """displays an error message"""
        x, y = self.GetPosition()
        wx.MessageBox(message, style=wx.OK | wx.CENTER, parent=self, x=x, y=y)
        return None

    def create_restaurant(self):
        """creates an Restaurant object to be saved to the database"""
        name = self.name_field.GetValue()
        cuisine = self.cuisine_field.GetValue()
        franchise = True if self.is_franchise.GetCurrentSelection() else False
        address = self.entered_addresses.GetItems()
        hours = {}
        hours['monday'] = [
            self.monday_opening_field.GetValue(), self.monday_closing_field.GetValue()
            ]
        hours['tuesday'] = [
            self.tuesday_opening_field.GetValue(), self.tuesday_closing_field.GetValue()
            ]
        hours['wednesday'] = [
            self.wednesday_opening_field.GetValue(), self.wednesday_closing_field.GetValue()
            ]
        hours['thursday'] = [
            self.thursday_opening_field.GetValue(), self.thursday_closing_field.GetValue()
            ]
        hours['friday'] = [
            self.friday_opening_field.GetValue(), self.friday_closing_field.GetValue()
            ]
        hours['saturday'] = [
            self.saturday_opening_field.GetValue(), self.saturday_closing_field.GetValue()
            ]
        hours['sunday'] = [
            self.sunday_opening_field.GetValue(), self.sunday_closing_field.GetValue()
            ]
        return Restaurant(name, cuisine, franchise, address, hours, self.temp_menus)

    def populate_form(self):
        """populate the editor with data"""
        with shelve.open(self.database) as db:
            restaurant = db[self.restaurant]
        self.name_field.SetValue(restaurant.name)
        self.cuisine_field.SetValue(restaurant.cuisine)
        if restaurant.isfranchise:
            self.is_franchise.SetSelection(1)
        for addr in restaurant.address:
            self.entered_addresses.Append(addr)
        self.monday_opening_field.SetValue(restaurant.hours['monday'][0])
        self.monday_closing_field.SetValue(restaurant.hours['monday'][1])
        self.tuesday_opening_field.SetValue(restaurant.hours['tuesday'][0])
        self.tuesday_closing_field.SetValue(restaurant.hours['tuesday'][1])
        self.wednesday_opening_field.SetValue(restaurant.hours['wednesday'][0])
        self.wednesday_closing_field.SetValue(restaurant.hours['wednesday'][1])
        self.thursday_opening_field.SetValue(restaurant.hours['thursday'][0])
        self.thursday_closing_field.SetValue(restaurant.hours['thursday'][1])
        self.friday_opening_field.SetValue(restaurant.hours['friday'][0])
        self.friday_closing_field.SetValue(restaurant.hours['friday'][1])
        self.saturday_opening_field.SetValue(restaurant.hours['saturday'][0])
        self.saturday_closing_field.SetValue(restaurant.hours['saturday'][1])
        self.sunday_opening_field.SetValue(restaurant.hours['sunday'][0])
        self.sunday_closing_field.SetValue(restaurant.hours['sunday'][1])
        for menu in restaurant.menus:
            self.menu_list.Append((menu.title, len(menu.items)))
            self.temp_menus.append(menu)
        return None


if __name__ == '__main__':
    app = wx.App()
    form = EditorGUI(
        None,
        database='restaurants',
        restaurant='Fiery Wok',
        datamap={},
        title='Editor Form'
        )
    form.ShowModal()
    app.MainLoop()

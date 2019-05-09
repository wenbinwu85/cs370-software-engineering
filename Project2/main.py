import shelve
import wx
import wx.adv
from gui import CustomerGUI, RestaurantGUI, EditorGUI


class MyApp(wx.App):
    """Custom app class"""
    def OnInit(self):
        self.ADMIN_ACCOUNT = ('admin', 'admin')  # hardcoded admin account
        self.is_admin = False
        self.frame = CustomerGUI(None, title='Restaurants Customer GUI')
        menubar = self.create_menubar()
        self.frame.SetMenuBar(menubar)
        self.frame.Show()
        return True

    def create_menubar(self):
        """Create a menubar for the app"""
        settings_menu = wx.Menu()
        sm_login = settings_menu.Append(-1, '&Admin Login')
        help_menu = wx.Menu()
        hm_about = help_menu.Append(wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.login_dialog, sm_login)
        self.Bind(wx.EVT_MENU, self.about_dialog, hm_about)
        menubar = wx.MenuBar()
        menubar.Append(settings_menu, '&Settings')
        menubar.Append(help_menu, '&Help')
        return menubar

    def login_dialog(self, event):
        """handler for admin login menu item"""
        dialog = wx.Dialog(self.frame, title='Administrator Login')
        dialog.CenterOnParent()

        # ----- username -----
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(dialog, -1, label='Username:')
        username_field = wx.TextCtrl(dialog)
        username_sizer.Add(username_label, 0, wx.ALL | wx.CENTER, 5)
        username_sizer.Add(username_field, 0, wx.ALL, 5)

        # ----- password -----
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(dialog, -1, label='Password:')
        password_field = wx.TextCtrl(dialog, style=wx.TE_PASSWORD)
        password_sizer.Add(password_label, 0, wx.ALL | wx.CENTER, 5)
        password_sizer.Add(password_field, 0, wx.ALL, 5)

        # ----- buttons -----
        button_sizer = wx.StdDialogButtonSizer()
        login_button = wx.Button(dialog, wx.ID_OK, label='Login')
        login_button.SetDefault()
        cancel_button = wx.Button(dialog, wx.ID_CANCEL)
        button_sizer.AddButton(login_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        # ----- main container -----
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(username_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(password_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Fit(dialog)
        dialog.SetSizer(main_sizer)

        if dialog.ShowModal() == wx.ID_OK:
            self.admin_login(username_field.GetValue(), password_field.GetValue())
        return None

    def about_dialog(self, event):
        """handler for about dialog box"""
        info = wx.adv.AboutDialogInfo()
        info.Name = 'Project 2'
        info.Version = 'v0.9.8'
        info.Copyright = '(c) 2019 Wenbin Wu\n' + \
                         'Email: dev@wuwenb.in\n' + \
                         'Github repo: https://github.com/wenbinwu85/cs370-software-engineering'
        info.Description = '' + \
            'Project 2 for CS370 Software Engineering Spring 2019.\n' + \
            'Professor: Dr. Sateesh Mane\n' + \
            'Objective: To create a GUI that displays restaurant menus.\n' + \
            'Written in Python3 and wxPython GUI package.\n'
        info.Developers = ['Wenbin Wu']
        info.License = 'Free for academic use.'
        wx.adv.AboutBox(info)
        return None

    def admin_login(self, username, password):
        """login to admin account"""
        if self.is_admin == True:
            return None
        if (username, password) == self.ADMIN_ACCOUNT:
            self.is_admin = True
            self.frame.SetTitle('Restaurants Administrator GUI')
            self.frame.SetStatusText('Successfully logged in. Administrator privilages granted.')

            # ----- unlock and display the admin functions -----
            self.admin_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.frame.panel, label='Administrator Funcitons')
            add_button = wx.Button(self.frame.panel, wx.ID_ADD)
            add_button.Bind(wx.EVT_BUTTON, self.add_restaurant)
            edit_button = wx.Button(self.frame.panel, wx.ID_EDIT)
            edit_button.Bind(wx.EVT_BUTTON, self.edit_restaurant)
            delete_button = wx.Button(self.frame.panel, wx.ID_DELETE)
            delete_button.Bind(wx.EVT_BUTTON, self.delete_restaurant)
            refresh_button = wx.Button(self.frame.panel, wx.ID_REFRESH)
            refresh_button.Bind(wx.EVT_BUTTON, self.reload_database)
            logout_button = wx.Button(self.frame.panel, label='Logout')
            logout_button.Bind(wx.EVT_BUTTON, self.admin_logout)
            self.admin_sizer.Add(add_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.admin_sizer.Add(edit_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.admin_sizer.Add(delete_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.admin_sizer.Add(refresh_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.admin_sizer.Add(logout_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            self.frame.main_sizer.Add(self.admin_sizer, 0, wx.ALL | wx.CENTER, 5)
            self.frame.panel.Layout()
            self.frame.SetSize((780, 460))
        return None

    def admin_logout(self, event):
        """logout of admin account"""
        self.is_admin = False
        self.frame.SetTitle('Restaurants Customer GUI')
        self.frame.SetStatusText('Successfully logged out. Currently in customer mode.')
        self.frame.main_sizer.Hide(self.admin_sizer)
        self.frame.main_sizer.Remove(self.admin_sizer)
        self.frame.panel.Layout()
        self.frame.SetSize((780, 380))
        return None

    def add_restaurant(self, event):
        """display the editor gui to add a new restaurant"""
        add_dialog = EditorGUI(
            self.frame,
            self.frame.database,
            datamap=self.frame.itemDataMap,
            title='Add Restaurant'
            )
        add_dialog.CenterOnParent()
        add_dialog.ShowWindowModal()
        return None

    def edit_restaurant(self, event):
        """display the editor gui to edit a selected restaurant"""
        index = self.frame.restaurant_list.GetFirstSelected()
        if index == -1:
            return None
        item = self.frame.restaurant_list.GetItem(index)
        restaurant = item.GetText()
        self.edit_dialog = EditorGUI(
            self.frame,
            self.frame.database,
            restaurant,
            datamap=self.frame.itemDataMap,
            title='Edit Restaurant'
            )
        self.edit_dialog.CenterOnParent()
        self.edit_dialog.ShowWindowModal()
        return None

    def delete_restaurant(self, event):
        """delete the selected restaurant"""
        index = self.frame.restaurant_list.GetFirstSelected()
        if index == -1:
            return None
        selected_name = self.frame.restaurant_list.GetItem(index, 0).GetText()
        selected_address = self.frame.restaurant_list.GetItem(index, 2).GetText()
        with shelve.open(self.frame.database) as db:
            for restaurant in db.values():
                if selected_address in restaurant.address:
                    if restaurant.isfranchise:
                        restaurant.address.remove(selected_address)
                        db[selected_name] = restaurant
                    else:
                        del db[selected_name]
        self.frame.restaurant_list.DeleteItem(index)
        self.frame.load()
        return None

    def reload_database(self, event):
        """reload the database data"""
        self.frame.load()
        return None

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()

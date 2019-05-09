import shelve
import wx
import wx.adv
from gui import LoginDialog, CustomerGUI, RestaurantGUI, EditorGUI


class MyApp(wx.App):
    """Custom app class"""
    def OnInit(self):
        self.ADMIN_ACCOUNT = ('admin', 'admin')  # hardcoded admin account
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
        dialog = LoginDialog(self.frame, title='Administrator Login')
        if dialog.ShowModal() == wx.ID_OK:
            username = dialog.username_field.GetValue()
            password = dialog.password_field.GetValue()
            if (username, password) == self.ADMIN_ACCOUNT:
                self.frame.admin_login()
        return None

    def about_dialog(self, event):
        """handler for about dialog box"""
        info = wx.adv.AboutDialogInfo()
        info.Name = 'Project 2'
        info.Version = 'v0.9.9'
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


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()

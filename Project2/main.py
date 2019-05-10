"""
main program file

Written by Wenbin Wu
"""

import shelve
import wx
import wx.adv
from gui import LoginDialog, CustomerGUI, RestaurantGUI, EditorGUI


class MyApp(wx.App):
    """Custom app class"""
    def OnInit(self):
        self.frame = CustomerGUI(None, title='Restaurants Customer GUI')
        menubar = self.create_menubar()
        self.frame.SetMenuBar(menubar)
        self.frame.Show()
        return True

    def create_menubar(self):
        """Create a menubar for the app"""
        help_menu = wx.Menu()
        hm_about = help_menu.Append(wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.about_dialog, hm_about)
        menubar = wx.MenuBar()
        menubar.Append(help_menu, '&Help')
        return menubar


    def about_dialog(self, event):
        """handler for about dialog box"""
        info = wx.adv.AboutDialogInfo()
        info.Name = 'Project 2'
        info.Version = 'v0.9.12'
        info.Copyright = '(c) 2019 Wenbin Wu\n' 
        info.Description = '' + \
            'Project 2 for CS370 Software Engineering Spring 2019.\n' + \
            'Professor: Dr. Sateesh Mane\n' + \
            'Written in Python3.7.3 with wxPython4.0.4.\n' + \
            'Binary built with pyinstaller3.4.\n\n' + \
            'Email: dev@wuwenb.in\n' + \
            'Github: https://github.com/wenbinwu85/'
        info.License = 'Free for academic use.'        
        wx.adv.AboutBox(info)
        return None


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()

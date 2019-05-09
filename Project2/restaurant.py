"""
This module contains classes for building a resturant object

Written by Wenbin Wu

"""


from dataclasses import dataclass


@dataclass
class Menu:
    title : str
    items : dict  # item : price

    def add_item(self, item, price):
        self.items[item] = price
        return None


@dataclass
class Restaurant:
    name : str
    cusine : str
    isfranchise : bool
    address : list  # list of address string: 'x, y'
    hours : dict  # key: day, value: [open hour, closing hour]
    menus : list  # list of Menu objects

    def add_menu(self, new_menu):
        if isinstance(new_menu, Menu):
            self.menus.append(new_menu)
        return None

    def get_info(self):
        info = (self.name, self.cusine, self.address, self.hours, self.menus)
        return info

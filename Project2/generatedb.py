"""
This module generates the initial database file.

The address for each restaurant location is randomly generated,
therefore each run of this module will create a slightly
different data set for the database.

Written by Wenbin Wu
"""

import shelve
import random
from restaurant import *


def make_random_address():
    """generate random address tuple"""
    x = random.randint(1, 99)
    y = random.randint(1, 99)
    return f'{x}, {y}'

def make_menu(menu_title, menu_data):
    """generate a restaurant menu from input data file"""
    menu = Menu(title=menu_title, items=dict())
    with open('./data/' + menu_data) as file:
        for row in file:
            data = eval(row)
            name, price = data
            menu.add_item(name, price)
    return menu

r1 = Restaurant(
    name="Jenny's Bakery",
    cuisine='Bakery',
    isfranchise=True,  # franchise can have more than one address
    address=[make_random_address(), make_random_address()],  # list of addresses
    hours={
        'monday': ['7:00AM', '9:00PM'],
        'tuesday': ['7:00AM', '9:00PM'],
        'wednesday': ['7:00AM', '9:00PM'],
        'thursday': ['7:00AM', '9:00PM'],
        'friday': ['7:00AM', '9:00PM'],
        'saturday': ['7:00AM', '9:00PM'],
        'sunday': ['7:00AM', '9:00PM']
        },
    menus=[make_menu('Baked Goods', 'r1_menu.txt')]
    )

r3 = Restaurant(
    name='Izza Pizzas',
    cuisine='Pizza',
    isfranchise=False,
    address=[make_random_address()],
    hours={
        'monday': ['10:00AM', '8:00PM'],
        'tuesday': ['10:00AM', '8:00PM'],
        'wednesday': ['10:00AM', '8:00PM'],
        'thursday': ['10:00AM', '8:00PM'],
        'friday': ['', 'Closed'],  # closed on Fridays
        'saturday': ['10:00AM', '8:00PM'],
        'sunday': ['10:00AM', '8:00PM']
        },
    menus=[make_menu('Pizzas / Wings', 'r3_menu.txt')]
    )

r4 = Restaurant(
    name="Ben's Grill",
    cuisine='Steakhouse',
    isfranchise=False,
    address=[make_random_address()],
    hours={
        'monday': ['10:00AM', '11:00PM'],
        'tuesday': ['10:00AM', '11:00PM'],
        'wednesday': ['10:00AM', '11:00PM'],
        'thursday': ['10:00AM', '11:00PM'],
        'friday': ['10:00AM', '12:00PM'],
        'saturday': ['10:00AM', '12:00PM'],
        'sunday': ['10:00AM', '12:00PM']
        },
    menus=[
        make_menu('Appitizers', 'r4_menu_appitizers.txt'),
        make_menu('Prime Meats', 'r4_menu_meats.txt'),
        ]
    )

r5 = Restaurant(
    name='Fiery Wok',
    cuisine='Chinese',
    isfranchise=False,
    address=[make_random_address()],
    hours={
        'monday': ['10:00AM', '7:00PM'],
        'tuesday': ['10:00AM', '7:00PM'],
        'wednesday': ['10:00AM', '7:00PM'],
        'thursday': ['10:00AM', '7:00PM'],
        'friday': ['10:00AM', '7:00PM'],
        'saturday': ['10:00AM', '7:00PM'],
        'sunday': ['10:00AM', '7:00PM']
        },
    menus=[
        make_menu('Lunch Specials', 'r5_menu_specials.txt'),
        make_menu('Stir Fries', 'r5_menu_stirfries.txt'),
        ]
    )

r6 = Restaurant(
    name='Yummy Curry House',
    cuisine='Indian',
    isfranchise=False,
    address=[make_random_address()],
    hours={
        'monday': ['7:00AM', '9:00PM'],
        'tuesday': ['7:00AM', '9:00PM'],
        'wednesday': ['7:00AM', '9:00PM'],
        'thursday': ['7:00AM', '9:00PM'],
        'friday': ['7:00AM', '9:00PM'],
        'saturday': ['7:00AM', '9:00PM'],
        'sunday': ['7:00AM', '9:00PM']
        },
    menus=[make_menu('Currys', 'r6_menu.txt')]
    )

r7 = Restaurant(
    name='Flushing Burgers',
    cuisine='Fast Food',
    isfranchise=False,
    address=[make_random_address()],
    hours={
        'monday': ['9:00AM', '10:00PM'],
        'tuesday': ['9:00AM', '10:00PM'],
        'wednesday': ['9:00AM', '10:00PM'],
        'thursday': ['9:00AM', '10:00PM'],
        'friday': ['9:00AM', '10:00PM'],
        'saturday': ['9:00AM', '10:00PM'],
        'sunday': ['9:00AM', '10:00PM']
        },
    menus=[
        make_menu('Burgers', 'r7_menu_burgers.txt'),
        make_menu('Kids Menu', 'r7_menu_kids.txt'),
        ]
    )

r8 = Restaurant(
    name='Evergreen Diner',
    cuisine='Diner',
    isfranchise=False,
    address=[make_random_address()],
    hours={
        'monday': ['0:00AM', '11:59PM'],
        'tuesday': ['0:00AM', '11:59PM'],
        'wednesday': ['0:00AM', '11:59PM'],
        'thursday': ['0:00AM', '11:59PM'],
        'friday': ['0:00AM', '11:59PM'],
        'saturday': ['0:00AM', '11:59PM'],
        'sunday': ['0:00AM', '11:59PM']
        },
    menus=[
        make_menu('Breakfast', 'r8_menu_breakfast.txt'),
        make_menu('Lunch / Dinner', 'r8_menu_lunch_dinner.txt'),
        make_menu('Desserts', 'r8_menu_dessert.txt')
        ]
    )

r9 = Restaurant(
    name="V's N F's",
    cuisine='Salads',
    isfranchise=False,
    address=[make_random_address()],
    hours={
        'monday': ['7:00AM', '9:00PM'],
        'tuesday': ['7:00AM', '9:00PM'],
        'wednesday': ['7:00AM', '9:00PM'],
        'thursday': ['7:00AM', '9:00PM'],
        'friday': ['7:00AM', '9:00PM'],
        'saturday': ['7:00AM', '9:00PM'],
        'sunday': ['7:00AM', '9:00PM']
        },
    menus=[make_menu('Salads', 'r9_menu.txt')]
)

r10 = Restaurant(
    name='The Drunken Pirates',
    cuisine='Seafood & Bar',
    isfranchise=False,
    address=[make_random_address()],
    hours={
        'monday': ['7:00AM', '11:00PM'],
        'tuesday': ['', 'Closed'],  # closed on Tuesdays
        'wednesday': ['7:00AM', '11:00PM'],
        'thursday': ['7:00AM', '11:00PM'],
        'friday': ['7:00AM', '11:00PM'],
        'saturday': ['7:00AM', '1:00AM'],
        'sunday': ['7:00AM', '1:00AM']
        },
    menus=[make_menu('Fresh Seafood', 'r10_menu.txt')]
    )

restaurants = [r1, r3, r4, r5, r6, r7, r8, r9, r10]

# save data to database
with shelve.open('restaurants', writeback=True) as db:
    for r in restaurants:
        db[r.name] = r

if __name__ == '__main__':
    print('done!')

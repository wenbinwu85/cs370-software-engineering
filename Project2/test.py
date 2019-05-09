import shelve


# ----- view entire database ------
with shelve.open('restaurants') as db:
    num = 1
    for name, restaurant in db.items():
        print(f'#{num}  name: {name}  |  cusine: {restaurant.cusine}  |  address: {restaurant.address}')
        for day, hours in restaurant.hours.items():
            print(f'\t{day},  {hours}')
        print('\t---------------------')
        for menu in restaurant.menus:
            print(f'\tMenus: {menu.title}, {len(menu.items)}')
            for item, price in menu.items.items():
                print(f'\t\t{item}\t{price}')
        print()
        num += 1
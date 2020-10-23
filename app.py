from collections import OrderedDict
import datetime
import sys
import os
import csv

from peewee import *

db = SqliteDatabase('inventory.db')
new_inventory = []

class Product(Model):
    #content
    product_id = AutoField()
    product_name = CharField(max_length= 255, unique= True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(default = datetime.datetime.now)

    class Meta:
        database = db


def read_csv():
    with open('inventory.csv', newline = '') as csvfile:
        reader = csv.DictReader(csvfile, delimiter =',')
        rows = list(reader)
        for row in rows:
            row['product_quantity'] = int(row['product_quantity'])
            row['product_price'] = int(row['product_price'].replace('$','').replace('.', ''))
            row['date_updated'] = datetime.datetime.strptime(row['date_updated'], '%m/%d/%Y')
        for row in rows:
            try:    
                Product.create(
                    product_name = row['product_name'],
                    product_quantity = row['product_quantity'],
                    product_price = row['product_price'],
                    date_updated = row['date_updated']
                ).save()
            except IntegrityError:
                temp = Product.get(product_name=row['product_name'])
                temp.product_name = row['product_name']
                temp.product_quantity = row['product_quantity']
                temp.product_price = row['product_price']
                temp.date_updated = row['date_updated']
                temp.save()
        

def menu_loop():
    user_input = None
    user_inputs = ['q', 'v', 'a', 'b']
    while user_input != 'q':
        clear()
        print("Justin's store inventory\n\n")
        print('Please choose one of the 3 options or put q to exit')
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        user_input = input('\nChoose an option: ').lower().strip()
        if user_input not in user_inputs:
            clear()
            print('That is not a correct option')
        elif user_input in menu:
            menu[user_input]()
        


def view_entry():
    """View Entry """
    clear()
    while True:   
        user_id = input('Please enter the product ID \n')
        try:
            user_id = int(user_id)
        except ValueError:
            clear()
            print('That is not a valid option. Please try agian.\n')
    
        entries = Product.select().where(Product.product_id == user_id)
        if entries:
            clear()
            print('Product ID: {}\n'.format(user_id))
            for entry in entries:
                print('Product name: {}\n'.format(entry.product_name))
                print('Product price: ${:.2f}\n'.format(float(entry.product_price) / 100))
                print('Product quantity: {}\n'.format(entry.product_quantity))
                print('Date updated: {}\n'.format(entry.date_updated))
            
        else:
            print('Sorry, that product ID does not exist')

        try_agian = input('Would you like to search for another item y/n? \n').lower()
        if try_agian == 'n':
            break
        
    


def add_entry():
    """Add an Entry"""
    new_name = input('Please tell us the name of the new item.\n')
    while True:
        new_quantity = input('How many items are there.\n')
        try:
            new_quantity = int(new_quantity)
            break
        except ValueError:
            print('Sorry please enter a number')

    while True:
        new_price = input('What is the price of the item.\n')
        try:
            new_price = float(new_price)
            new_price = int(new_price * 100)
            break
        except ValueError:
            print('Sorry please enter a number')
    try:
        Product.create(
                    product_name = new_name,
                    product_quantity = new_quantity,
                    product_price = new_price,
                    date_updated = datetime.datetime.now()
                ).save()
    except IntegrityError:
        temp = Product.get(product_name=new_name)
        temp.product_quantity = new_quantity
        temp.product_price = new_price
        temp.date_updated = datetime.datetime.now()
        temp.save()
        

        



    


def backup_data():
    """Backup Data"""
    pass
    

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    db.connect()
    db.create_tables([Product], safe = True)
    read_csv()
    menu_loop()


menu = OrderedDict([
    ('v', view_entry),
    ('a', add_entry),
    ('b', backup_data),
])  


if __name__ == '__main__':
    clear()
    initialize()
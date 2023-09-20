import csv
import copy
class Store:
    available_items = {}
    def __init__(self, item, price, quantity):
        self.item = item
        self.price = price
        self.quantity = quantity
        
        Store.available_items.update({
            self.item:{
                'price':self.price,
                'quantity':self.quantity
            }
        })    
    @classmethod
    def create_instances(cls, file):
        with open(file, 'r') as items_file:
            reader = csv.DictReader(items_file)
            items = list(reader)
        for item in items:
            Store(
                item.get('item'),
                int(item.get('price')),
                int(item.get('quantity'))
            )   

    @classmethod
    def show_available_items(cls):
        all_items = Store.available_items
        available_items = [item for item in all_items if all_items[item]['quantity'] !=0 ]
        for i, item in enumerate(available_items):
            print(f'{i+1}: {item}')            

class Customer:
    cart = {}
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f'{self.name}'
    @classmethod
    def add_to_cart(cls, dict_item):
        Customer.cart.update(dict_item)
        
    def view_cart(self, cart):
        total_price = 0
        for item in cart:
            quantity = cart[item]['quantity']
            price = cart[item]['price'] * quantity
            total_price += price
            print(f'{item}: X{quantity} for ${price:.2f}')
        print(f'Your total cart price is: ${total_price:.2f}')    

    def add_item_to_file(self, file_name, row):
        with open(file_name, 'a') as customers:
            writer = csv.writer(customers)
            writer.writerow(row)

    def remove_item_from_file(self, file_name, customer_name):
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            reader = list(reader)
        customers_data = []
        for row in reader:
            if (customer_name not in row) and row:
                customers_data.append(row)
        with open(file_name, 'w') as new_data:
            writer = csv.writer(new_data)
            writer.writerows(customers_data)
    def show_cart_total_price(self, cart):
        total_price = 0
        for item in cart:
            quantity = cart[item]['quantity']
            price = cart[item]['price'] * quantity
            total_price += price
        print(f'Your total cart price is: ${total_price:.2f}')

    def clear_cart(self, cart):
        Customer.cart.clear()
        print('Cart has been succesfully cleared')
def greet_user():
    print('Welcome to Moh_hatem online store')

def show_choices():
    print('''What would you like to do?
1. Show available items
2. View cart
3. View total cart price
4. Clear cart
5. Quit''')

def show_available_items():
    items = Store.available_items
    items_names = list(items)
    Store.show_available_items()
    try:
        choice = int(input('Enter the number of item you want to purchase (0 to return to menu): '))
    except ValueError:
        print('only numbers allowed')
        return
    if choice == 0:
        return
    elif choice not in range(1, (len(items)+1) ):
       print('Please choose a valid number')
    else:
        item = items_names[choice -1]        
        store_quantity = items[item]['quantity']
        quantity = int(input('Enter the quantity: '))    
        if store_quantity < quantity:
            print(f'Sorry we only have {store_quantity} of this item')
        else:
            items[item]['quantity'] -= quantity
            print('{item} has been added'.format(item=item))
            return {
                item:{
                    'price':items[item]['price'],
                    'quantity':quantity
                }
            }
            
def main():
    greet_user()
    name = input('Enter your name: ')
    customer = Customer(name)
    Store.create_instances('items.csv')
    items_copied = copy.deepcopy(Store.available_items)
    while True:
        show_choices()     
        choice = input('Enter your choice: ')
        if choice == '1':
            item_bought = show_available_items()
            if item_bought:
                Customer.add_to_cart(item_bought)
                key = list(item_bought.keys())
                item_name = key[0]
                price = item_bought[item_name]['quantity'] * item_bought[item_name]['price']
                row = [customer, item_name, price]
                customer.add_item_to_file('customers.csv', [])
                customer.add_item_to_file('customers.csv', row)
        elif choice == '2':
            cart = Customer.cart
            if cart:
                customer.view_cart(cart)
            else:
                print('Your cart is empty')    
        elif choice == '3':
            cart = Customer.cart
            if cart:
                customer.show_cart_total_price(cart)
            else:
                print('Your cart is empty')
        elif choice == '4':
            cart = Customer.cart
            if cart:
                submit = input('are you sure you want to clear the cart (y/n)?: ').lower()
                if submit != 'n':
                    customer.clear_cart(cart)
                    customer.remove_item_from_file('customers.csv',name)
                    Store.available_items = items_copied
                else:
                    continue    
            else:
                print('Sorry, your cart is already empty')
        elif choice == '5':
            print('Thanks for visiting Moh_hatem online shop')
            break
        else:
            print('Invalid option, please try again')

main()
import queue, threading, time
# act like a customer and order the required materials from the store. then take qty away from the inventory and pull pricing 
# use time module to sleep one second to act like system searching for item in system

inventory = {'pen': 15, 
             'pencil': 7, 
             'paper': 200, 
             'backpack': 5, 
             'divider': 50, 
             'stapler': 15}

cost_item = {'pen': 2.99, 
             'pencil': 1.49, 
             'paper': 3.15, 
             'backpack': 45.95, 
             'divider': 8.29, 
             'stapler': 13.67}

larry = {'pen': 1, 
         'paper': 25, 
         'divider': 4}

def find_price(customer): # Customer side
    items = list(customer.keys())
    cart_bill = 0
    for item in items:
        item_price = cost_item[item]
        cart_bill += item_price
    return cart_bill

def find_inventory(customer): # business side
    for k, v in customer.items():
        print(f'searching for {k}...')
        time.sleep(2) # simulates the system taking a while to load
        print(f'found {k} with a stock level of {v}')
        time.sleep(1)
        inventory[k] = inventory[k] - v
        if inventory[k] <= 0:
            inventory[k] = inventory[k] + v
            print(f'Could not fulfill order for {k} of {v}')

x = find_inventory(larry)
print(inventory)
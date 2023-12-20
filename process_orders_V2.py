import threading
import queue
import time

print_lock = threading.Lock()

# Worker function to process items from the queue
def worker(q):
    total_cost = 0
    while True:
        item, qty = q.get()  # Retrieve item and value from the queue
        total_cost += cost_item[item]
        find_inventory(item, qty)  # Perform the task
        q.task_done()  # Mark the task as done
 
 # process item in business inventory
def find_inventory(item, qty): # business side
    with print_lock:
        print(f'searching for {item}...')
    time.sleep(2) # simulates the system taking a while to load
    with print_lock:
        print(f'found {item} with a stock level of {qty}')
    time.sleep(1)
    with print_lock:
        inventory[item] = inventory[item] - qty
        if inventory[item] <= 0:
            inventory[item] = inventory[item] + qty
            print(f'Could not fulfill order for {item} of {qty}')


# Data
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

# Creating a queue instance
order_queue = queue.Queue()

# Creating and starting threads
num_threads = 3
for _ in range(num_threads):
    t = threading.Thread(target=worker, args=(order_queue,))
    t.daemon = True  # Set threads as daemon so they'll exit when the main program exits
    t.start()

# Adding tasks to the queue
cust_order = [('pen', 1), 
             ('paper', 25), 
             ('divider', 4)]

for item in cust_order:
    order_queue.put(item)  # Enqueue tasks into the queue

# Wait for all tasks to be completed
order_queue.join()
print("Order completed.")

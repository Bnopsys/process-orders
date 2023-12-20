# Threading/Queues Functional Project
#### Applying the concepts of Threading and Queues to a familiar setting: Logistics

### 1. Creating a worker function
The goal of this project was to use multithreading and queues with information thats easier for me to understand. So i just used a situation that's familiar with me. 
```python
def worker(q):
    total_cost = 0
    while True:
        item, qty = q.get()  # Retrieve item and value from the queue
        total_cost += cost_item[item]
        find_inventory(item, qty)  # Perform the task
        q.task_done()  # Mark the task as done
```
This function is the worker which does two main operations: Calculates the total cost for the order and 'grabs' the items from stock.

### 2. Grabbing from stock function
```python
print_lock = threading.Lock()

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
```
The print lock establishes a lock on the threads so that everything comes out in order rather than printing on the same line like before it was added. The top few lines are just to make the function I/O bound by adding time.sleeps to simulate the system taking time to process the orders. But the last few lines is the only calculation for the function: removing the amount ordered from the inventory stock. Then there is an if statement to check if by lowering the stock quantity it would be zero or under. And if so we just reverse it and tell the customer that it couldn't be fulfilled.

### 3. Creating the queue and threads
After creating the queue and setting the max number of threads, we use a for loop for starting all the threads. The '_' used is a throwaway variable since I didn't need it besides looping over the threads. Then we create threads with the worker function as the target and adding its argument inside the args with a comma after to have it a tuple(required for python). 
```python
# Creating a queue instance
order_queue = queue.Queue()

# Creating and starting threads
num_threads = 3
for _ in range(num_threads):
    t = threading.Thread(target=worker, args=(order_queue,))
    t.daemon = True  # Set threads as daemon so they'll exit when the main program exits
    t.start()
```

### 4. Adding tasks to the queue
This shows the customers order and then adds them to the queue with a for loop. Lastly since the queue has already started I joined the threads and waited for them to complete before printing Order Complete.

```python
cust_order = [('pen', 1), 
             ('paper', 25), 
             ('divider', 4)]

for item in cust_order:
    order_queue.put(item)  # Enqueue tasks into the queue

# Wait for all tasks to be completed
order_queue.join()
print("Order completed.")
```
## Concepts learned for this project
### Threads
Threads are the lowest level of work done in the os, which can be executed independently of other code. And as a subset of processes, Threads are not limited to one per process. 
### Multithreading
The definition of multithreading is the ability of the processor running threads concurrently. Different threads can be loaded and start up their process giving the fallacy that threads can be run at the same time. But it is actually due to those interrupts which lets the threads to switch and start a new task while the other is waiting (I/O or CPU tasks).

### ThreadpoolExecutor 
This alternate way of utilizing threads is an improvement on one main part. Threads are destroyed after being created which takes significant CPU usage. Threadpool on the otherhand creates a number set by the user. Then the requests are pulled from the pool and returned to the pool after the completion of a task.

### Queues
Queues are a data structure that are similar to lists in that they store data, and there are various types explained below:
* First In First Out(FIFO): Similar to lines used in stores, the first person who enters the line is the first person served. New elements are only able to enter the queue from the tail side and leave on the head side.
* Bounded FIFO: These are similar to normal FIFO queues except that there is a limit set on how many elements can be inside the queue at anytime and once that number is reached any future elements are rejected.
    * Bounded FIFO Overwrite: Overwrite removes the first element and adds a new item to the tail end to maintain the a set number of elements. 
    * Bounded FIFO Bounce: Just like specified above the Bounce is when after the queue has been saturated no more new elements can enter.
* Last In First Out(LIFO): Similar to dishes, the first dish is placed in the sink and newer dishes are placed above them which will in turn be washed before the last one.
* Deque: A double ended queue takes the attributes from both FIFO and LIFO to make a queue that can work elements from either side at anytime. A real world example of a Deque is at a hosiptal how people line up to get treated(FIFO) but if someone comes in with a life threatening condition they have to be seen first(LIFO). 
    * Rotate left/Rotate Right: This means to move all the elements of the queue either left or right.
* Priority Queue: These queues use conditions to determine who to move to the front and let out of the queue first. Think of boarding an airplane, everyone waits in line to board except for military, disabled, families with kids, first class, business class. These exceptions skip the line while the rest wait until they can board normally.

### Global Interpreter Lock(GIL)
The GIL is a mutex that prevents multiple threads from executing python bytecode at the same time. At any one time, a thread will hold the GIL and perform operations. Only once the task is complete, or there is a I/O bound task for the thread (time.sleep(), reading data, etc..) will the lock be released for other threads to grab and start their work.
##### Pros 
* Faster with single threaded operation
* Faster with multithreaded operation for I/O bound programs
* It makes wrapping C libraries easier since you don't have to worry about thread-safety

##### Cons
* Slows down the processing of CPU intensive work in python
* Stops other threads from working when a single thread holds the GIL for too long leading to a bottleneck

##### What to do if the GIL is an issue for your code
* By utilizing multiprocessing, each process has its own memory space and GIL allowing it to run in true parallel.
* Asynchronous programming doesn't use threads or processes and instead looks for I/O bound stoppages and uses that point as a trigger to switch to the next task.
* Other programming languages like C, C++, and Rust don't have a GIL so they can be utilized with python by integrating their libraries to python using ctypes, Cython, or CFFI. 

Sources: 
1. https://geeksta.net/geeklog/python-gil-pros-and-cons/
2. https://softwareengineering.stackexchange.com/questions/186889/why-was-python-written-with-the-gil
3. https://realpython.com/queue-in-python/


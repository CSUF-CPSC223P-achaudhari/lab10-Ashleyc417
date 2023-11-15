import threading
import time
import json

with open('inventory.dat', "r") as file:
    file_contents = json.load(file)

# Add items to cart
def bot_clerk(items, cart=list(), lock=threading.Lock()):

    # List of fetcher lists (nested)
    fetchers = [[],[], []]

    # Separate items into each fetcher list
    for i, item in enumerate(items):
        fetchers[i % 3].append(item)

    # Make bot fetch items assigned to it
    def bot_fetcher(items, cart, lock):
        for item in items:
            # "Sleep" to simulate robot moving to item
            time.sleep(int((file_contents[item])[1]))
            with lock:
                # Add item and item description to cart
                cart.append([item, (file_contents[item])[0]])

    # Launch each bot fetcher
    threads = []
    for i, fetcher in enumerate(fetchers):
        thread = threading.Thread(target=bot_fetcher, args=(fetcher, cart, lock))
        thread.start()
        threads.append(thread)

    # Wait for each thread to finish
    for thread in threads:
        thread.join()

    # Returns final cart with items and descriptions
    return cart
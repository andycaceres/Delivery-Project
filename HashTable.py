#Citation: 7.8 Python: Hash tables. Zybooks. (n.d.). Retrieved June 28, 2022, from 
#               https://learn.zybooks.com/zybook/WGUC950AY20182019/chapter/7/section/8 
# Used for the Hashtable


class HashTable:

    def __init__(self, initial_capacity = 40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])


    # Inserts a new item into the hash table. Big O(N)
    def insert(self, key, item):
        # get the bucket list where this item will go.
        length = len(self.table)
        bucket = int(key) % length
        bucket_list = self.table[bucket]

        '''# update if already exists
        for kv in bucket_list:
            if int(kv[0]) == key:
                kv[1] = item
                return True'''

        # insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True
         
    # Searches for an item with matching key in the hash table. Big O(N)
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        length = len(self.table)
        hash_key = hash(key)
        bucket = hash(int(key)) % length
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for key_value in bucket_list:
            if int(key_value[0]) == key:
                return key_value[1]
        
        return None

    # Removes an item with matching key from the hash table. Big O(N)
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv[0], kv[1])
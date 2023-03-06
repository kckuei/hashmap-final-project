# Name:         Kevin Kuei
# OSU Email:    kueik@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment:   Set 6
# Due Date:     3/17/23
# Description:  Implements a hashmap using open addressing with quadratic probing
#               for collision resolution inside the dynamic array.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #
    def find_slot(self, key: str) -> int:
        """
        Helper function to find the index of key, if present in the hashmap. If the
        key is not present, it returns the index of the first empty slot instead.
        Uses quadratic probing.
        """
        # Search until we either find the key or find an empty slot using
        # quadratic probing.
        i_initial = i = self._hash_function(key) % self._capacity
        j = 1
        while True:
            # ... if we find an empty slot.
            if self._buckets[i] is None:
                break
            # ... if we find the key and the entry is not a tombstone.
            if self._buckets[i].is_tombstone is False and self._buckets[i].key == key:
                break
            i = (i_initial + j ** 2) % self._capacity
            j += 1
        return i

    def find_first_avail_slot(self, key: str) -> int:
        """
        Helper function to find the index of first available slot, which can be
        either an empty slot (None) or tombstone.
        Uses quadratic probing.
        """
        # Search until we either find the key or find an empty slot using
        # quadratic probing.
        i_initial = i = self._hash_function(key) % self._capacity
        j = 1
        while True:
            # ... if we find an empty slot or tombstone.
            if self._buckets[i] is None or self._buckets[i].is_tombstone:
                break
            i = (i_initial + j ** 2) % self._capacity
            j += 1
        return i

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key
        already exists in the hash map, its associated value is replaced
        with the new value. If the given key is not in the hash map, a
        new key/value pair is added.

        The table is resized to double its current capacity when this
        method is called and the current load factor of the table is
        greater than or equal to 0.5.
        """
        # Check the load factor and double the array size if it exceeds 0.5.
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        # Get the initial hash. If the slot is empty, insert and return.
        i = self._hash_function(key) % self._capacity
        if self._buckets[i] is None:
            self._buckets[i] = HashEntry(key, value)
            self._size += 1
            return

        # Otherwise use quadratic probing to find our key in the hashmap.
        # Note: status will be either true or false.
        status = self.contains_key(key)
        # ...if we find the key, update the value and return.
        if status:
            i = self.find_slot(key)
            self._buckets[i].value = value
            return
        # ...otherwise, find the first available slot to place our key/value.
        else:
            i = self.find_first_avail_slot(key)
            # ...if we have an empty slot, insert a new hash entry.
            if self._buckets[i] is None:
                self._buckets[i] = HashEntry(key, value)
            # ...otherwise, we have a tombstone value, so update the key/value
            # and unmake the tombstone.
            else:
                self._buckets[i].key = key
                self._buckets[i].value = value
                self._buckets[i].is_tombstone = False
            self._size += 1
            return

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        # Count the empty buckets.
        count = 0
        for i in range(self._capacity):
            bucket = self._buckets[i]
            if bucket is None:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing
        key/value pairs remain in the new hash map, and all hash table
        links are rehashed. Tombstones are not copied over.

        The method does nothing if new_capacity less than the current
        number of elements in the hash map. If new_capacity is valid,
        checks if it is a prime number and makes it the next highest if not.
        """
        # Capacity must be larger than current number of elements.
        if new_capacity < self._size:
            return

        # Capacity must be a prime number.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # DYNAMIC ARRAY IMPLEMENTATION 1
        # Save the previous buckets.
        prev_buckets = self._buckets

        # Initialize new dynamic array with the new capacity, and reset
        # the size attribute.
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

        # Loop over the previous buckets, copying over key/value pairs
        # to the new hashmap wherever a valid (non-tombstone) item is found.
        for i in range(prev_buckets.length()):
            slot = prev_buckets[i]
            if slot is not None or (slot is not None and slot.is_tombstone is False):
                self.put(slot.key, slot.value)

        # # HASHMAP IMPLEMENTATION 2 (Alternative)
        # # Rehash all buckets into new hashmap.
        # hashmap = HashMap(new_capacity, self._hash_function)
        # for i in range(self._capacity):
        #     bucket = self._buckets[i]
        #     # Bypass empty buckets and tombstones.
        #     if bucket is not None and bucket.is_tombstone is False:
        #         hashmap.put(bucket.key, bucket.value)
        #
        # # Copy new hashmap buckets and attributes to current.
        # self._buckets = hashmap._buckets
        # self._capacity = hashmap._capacity
        # self._size = hashmap._size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is
        not in the hash map, the method returns None.
        """
        if self.contains_key(key):
            i = self.find_slot(key)
            return self._buckets[i].value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it
        returns False. An empty hash map does not contain any keys.
        """
        if self._size == 0:
            return False

        m = self._capacity
        i_initial = i = self._hash_function(key) % m
        j = 1
        while True:
            # ... if we find an empty slot.
            if self._buckets[i] is None:
                return False
            # ... if we find the key and the entry is not a tombstone.
            if not self._buckets[i].is_tombstone and self._buckets[i].key == key:
                return True
            i = (i_initial + j ** 2) % m
            j += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """
        i = self.find_slot(key)

        # Do nothing if the key is not in the hashmap.
        if self._buckets[i] is None:
            return

        # Otherwise, set the tombstone to true and decrement hash map size.
        self._buckets[i].is_tombstone = True
        self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the
        underlying hash table capacity.
        """
        for i in range(self._capacity):
            self._buckets[i] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map. The results are unsorted.
        """
        da = DynamicArray()
        for slot in self:
            if slot is not None and not slot.is_tombstone:
                da.append((slot.key, slot.value))
        return da

    def __iter__(self):
        """
        Enables the hash map to iterate across itself. Builds the
        iterator functionality inside the HashMap class.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Return the next item in the hash map, based on the current
        location of the iterator.
        """
        while True:
            if self._index == self._capacity:
                raise StopIteration
            slot = self._buckets[self._index]
            self._index += 1
            if slot is not None and not slot.is_tombstone:
                break
        return slot

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

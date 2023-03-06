# Name:         Kevin Kuei
# OSU Email:    kueik@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment:   Set 6
# Due Date:     3/17/23
# Description:  Implements a hashmap using separate chaining (linked-lists)
#               for collision resolution inside the dynamic array.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key
        already exists in the hash map, its associated value is replaced
        with the new value. If the given key is not in the hash map, a
        new key/value pair is added.

        The table is resized to double its current capacity when this
        method is called and the current load factor of the table is >= 1.0.
        """
        # ~Doubles the array capacity if the load factor exceeds unity.
        # Note: .resize_table() guarantees the capacity will be a prime number.
        if self.table_load() >= 1.0:
            self.resize_table(2 * self._capacity)

        # Now we need to update the key/value pair.
        # First get the bucket/link-list.
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        # Check if the linked-list contains our key.
        # Note: .contains() will return either None, or the node of the key.
        node = bucket.contains(key)

        # If node is None, we didn't find our key, so insert a new node and
        # update hash map size.
        if node is None:
            bucket.insert(key, value)
            self._size += 1
        # Otherwise, we found our key, so update the node value.
        else:
            node.value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        # Sums the empty buckets of the hashmap.
        counts = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                counts += 1
        return counts

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        # Load factor = elements/buckets = size/capacity.
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change the underlying
        hash table capacity.
        """
        # Clears the hashmap buckets.
        for i in range(self._capacity):
            self._buckets[i].__init__()

        # Resets the hashmap size.
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing
        key/value pairs remain in the new hash map, and all hash table
        links are rehashed.

        Checks that new_capacity is not less than 1; if so, the method
        does nothing. If new_capacity is 1 or more, checks if prime number.
        If not, changes it to the next highest prime number.
        """
        # Capacity must be at least 1.
        if new_capacity < 1:
            return

        # Capacity must be a prime number.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # DYNAMIC ARRAY IMPLEMENTATION 1 (Passes Gradescope)
        # Save previous buckets.
        prev_buckets = self._buckets

        # Re-init buckets with new capacity, and reset size.
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

        # Rehash previous key/value pairs from old buckets into new.
        for i in range(prev_buckets.length()):
            linked_list = prev_buckets[i]
            for node in linked_list:
                self.put(node.key, node.value)

    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is
        not in the hash map, the method returns None.
        """
        # Check the bucket/link if it contains are key.
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        node = bucket.contains(key)

        # Only return a value if we get back a node.
        if node is not None:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it
        returns False. An empty hash map does not contain any keys.
        """
        # Returns true unless the hashmap is empty or the key doesn't exist.
        if (self._size == 0) or (self.get(key) is None):
            return False
        return True

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """
        # Gets the bucket/linked-list.
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]

        # Remove the node from the bucket/linked-list, if present.
        status = linked_list.remove(key)

        # If the remove is successful, decrement the hashmap size.
        if status is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map.

        The order of the keys in the dynamic array does not matter.
        """
        # Loop over the hashmap buckets/linked-lists and nodes, appending
        # key/value pairs as tuples to the output array.
        da = DynamicArray()
        for i in range(self._capacity):
            for node in self._buckets[i]:
                da.append((node.key, node.value))
        return da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a dynamic (unsorted) array, and returns a tuple containing,
    in this order, a dynamic array comprising the mode (most occurring)
    value/s of the array, and an integer that represents the highest
    frequency (how many times the mode value(s) appear).

    If there is more than one value with the highest frequency, all values
    at that frequency are included in the array being returned (any order).
    If there is only one mode, the dynamic array will only contain that value.

    Assumes array will contain at least one element, and that all values
    stored in the array will be strings.

    Runs in O(N) complexity.
    """
    # Loop over the input array and tally the numbers in a counts hashmap
    # while also tracking the maximum count. Executes in O(N).
    count_map = HashMap()
    max_count = 0
    for i in range(da.length()):
        # Increments the counts.
        key = str(da[i])
        count = count_map.get(key)
        if count is None:
            count = 1
        else:
            count += 1
        count_map.put(key, count)

        # Update max frequency.
        max_count = max(count, max_count)

    # Loop over the input array a 2nd time and record appends in an appends hashmap.
    # Only add values if the count is the max count and has not already been added.
    # Executes in O(n).
    append_map = HashMap()
    da_out = DynamicArray()
    for i in range(da.length()):
        key = str(da[i])
        count, append_flag = count_map.get(key), append_map.get(key)
        if count == max_count and append_flag is None:
            da_out.append(da[i])
            append_map.put(key, count)

    # Return the array of modes and max count.
    return da_out, max_count


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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")


# ------------------------------------------------------------------------------------------

    # print("\nPDF - Office Hour Example")
    # print("----------------------")
    # m = HashMap(1, hash_function_2)
    # key_value_pairs = [(798, 444), (998, -219), (153, 773), (695, -188), (307, 54)]
    # for key, value in key_value_pairs:
    #     m.put(str(key), value)
    #     print(f"Load factor: {m.table_load():.2f}, "
    #           f"Capacity: {m.get_capacity()},"
    #           f"Next Largest Prime: {m._next_prime(m.get_capacity()+1)}")
    # print('Output:\n'+str(m))
    # n = """
    # 0: SLL[]
    # 1: SLL[]
    # 2: SLL[(key798: 444)]
    # 3: SLL[]
    # 4: SLL[(key998: -219)]
    # 5: SLL[]
    # 6: SLL[]
    # 7: SLL[]
    # 8: SLL[]
    # 9: SLL[(key153: 773) -> (key695: -188)]
    # 10: SLL[(key307: 54)]
    # """
    # print('Expect:\n'+str(n))
    # print('Output:', 'Size', m.get_size(), 'Capacity', m.get_capacity())
    # print('Expect:', 'Size', 5, 'Capacity', 7)
    #
    # print("\nCustom Test 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_2)
    # key_value_pairs = [(316, -817), (740, 156), (545, 208),
    #                    (924, 406), (99, -609), (891, -921),
    #                    (929, 722), (968, 279),  (887, 246),
    #                    (300, -487), (403, 239),  (520, -959)]
    # for key, value in key_value_pairs:
    #     m.put(str(key), value)
    #     print('Load factor:', m.table_load())
    # print('Output:\n'+str(m))
    # n = """
    # 0: SLL [(key316: -817)]
    # 1: SLL [(key740: 156)]
    # 2: SLL []
    # 3: SLL []
    # 4: SLL [(key545: 208)]
    # 5: SLL [(key924: 406)]
    # 6: SLL [(key99: -609)]
    # 7: SLL []
    # 8: SLL [(key891: -921)]
    # 9: SLL []
    # 10: SLL [(key929: 722)]
    # 11: SLL []
    # 12: SLL []
    # 13: SLL [(key968: 279) -> (key887: 246)]
    # 14: SLL []
    # 15: SLL []
    # 16: SLL [(key300: -487)]
    # 17: SLL []
    # 18: SLL []
    # 19: SLL []
    # 20: SLL [(key520: -959) -> (key403: 239)]
    # 21: SLL []
    # 22: SLL []"""
    # print('Expect:\n'+str(n))
    # print('Output:', 'Size', m.get_size(), 'Capacity', m.get_capacity())
    # print('Expect:', 'Size', 12, 'Capacity', 23)
    #
    # print("\nCustom Test 2")
    # print("----------------------")
    # # 3, 5*, 7, 11*, 17, 19, 23*
    # m = HashMap(23, hash_function_2)
    # key_value_pairs = [(104, -860), (222, 789) , (151, -718), (520, 286), (115, 832),
    #                    (440, -691), (550, -787), (65, 641), (712, 147), (605, -678),
    #                    (254, -425), (533, -753), (561, -343), (751, 30), (409, 745),
    #                    (761, -664), (825, 650), (591, 536), (88, -675), (475, -474),
    #                    (765, -606), (693, -656), (828, 23), (299, 802), (884, 926),
    #                    (759, -737), (786, 703)]
    # for key, value in key_value_pairs:
    #     m.put(str(key), value)
    #     print('Load factor:', m.table_load())
    #     # if m.table_load() >= 1.0:
    #     #     print('Capacity:', m.get_capacity())
    #     #     print('Next Largest Prime:', m._next_prime(m.get_capacity() + 1))
    # print('Output:\n'+str(m))
    # n = """
    # 0: SLL [(key440: -691)]
    # 1: SLL []
    # 2: SLL [(key550: -787) -> (key712: 147)]
    # 3: SLL [(key605: -678) -> (key254: -425) -> (key533: -753)]
    # 4: SLL [(key561: -343)]
    # 5: SLL [(key751: 30) -> (key409: 745)]
    # 6: SLL [(key761: -664)]
    # 7: SLL [(key591: 536) -> (key825: 650)]
    # 8: SLL [(key475: -474)]
    # 9: SLL []
    # 10: SLL [(key828: 23) -> (key693: -656) -> (key765: -606)]
    # 11: SLL []
    # 12: SLL [(key884: 926) -> (key299: 802)]
    # 13: SLL [(key786: 703) -> (key759: -737)]
    # 14: SLL []
    # 15: SLL []
    # 16: SLL []
    # 17: SLL []
    # 18: SLL []
    # 19: SLL []
    # 20: SLL []
    # 21: SLL []
    # 22: SLL []
    # 23: SLL []
    # 24: SLL []
    # 25: SLL []
    # 26: SLL []
    # 27: SLL []
    # 28: SLL []
    # 29: SLL [(key65: 641)]
    # 30: SLL []
    # 31: SLL []
    # 32: SLL []
    # 33: SLL []
    # 34: SLL [(key88: -675) -> (key104: -860)]
    # 35: SLL [(key222: 789)]
    # 36: SLL [(key115: 832) -> (key520: 286) -> (key151: -718)]
    # """
    # print('Expect:\n'+str(n))
    # print('Output:', 'Size', m.get_size(), 'Capacity', m.get_capacity())
    # print('Expect:', 'Size', 27, 'Capacity', 37)






# Data Structures Final Project: Hash Table/Map

## Motivation
* Why use [hash tables](https://en.wikipedia.org/wiki/Hash_table)? The most valuable aspect of a hash table over other abstract data structures is its speed to perform insertion, deletion, and search operations. Hash tables can do them all on average, with constant time.


**Hash table time complexity in big o notation**
| Algorithm  | Average | Worse Case |
| ------------- | ------------- | ------------- |
| Algorithm  | Θ(n)  | O(n)  |
| Space      | Θ(1)  | O(n)  |
| Search     | Θ(1)  | O(n)  |
| Insert     | Θ(1)  | O(n)  |
| Delete     | Θ(1)  | O(n)  |


## Project Overview
* Data structures final project written in `python` which implements a `HashMap` class using two different approaches for collision resolution: 
	1) Seperate Chaining (SC); and 
	2) Open Addressing (OA) with Quadratic Probing.
* `HashMap` classes are implemented for SC and OA using the `DynamicArray` and singly `LinkedList` (SLL) classes provided in `a6_include.py`. These classes represent reduced data structures implemented earlier in the course.
* `HashMap` methods implemented: 
    * `put()` - updates an existing key or inserts a new key/value pair if the key is not found, resizing to maintain max allowable load factor constraints.
    * `empty_buckets()` - returns the number of empty buckets.
    * `table_load()` - returns the load factor.
    * `clear()` - clears the hash table.
    * `resize_table()` - resizes the hash table to a capacity that is prime numbered, copies over key/value pairs, and rehashes the links.
    * `get()` - returns the value associated with a key.
    * `contains_key()` - checks if a key is present.
    * `remove()` - removes a key/value pair.
    * `get_keys_and_values()` - returns an array of key/value tuples.
    * `find_mode()` - returns the mode of an array (SC only).
    * `__iter__()`, `__next__()`  - iterator implementation (OA only).

## Hash Table Concepts
* Hashmaps can be used to implement the dictionary ADT with key/value pairs.
* Think of hashmaps as basically a table of buckets or slots to hold values. 
* The principle mechanics to be understood are hashing for the insertion index, and resolution of colliding indices for different key/value pairs.
* To get the insertion index/address for a value, we hash the key (e.g. string, struct, double, etc.) to obtain an integer value:
	* `index = hash_func(key) % m`, where `m` is the capacity of the table.
	* Note the mod is to wrap the hash result such that `index <= m`. 
* Hash functions
	* The desirable properties of a hash function are:
		* Determinism - a given input always maps to the same hash value.
		* Uniformity - the inputs should be mapped as evenly as possible over the output range (prime number sizes tend to yield more uniform mappings).
		* Speed - the function should have a low computational burden.
	* A perfect hash function is one that results in no collisions;  in other words, every input gets a unique output.
	* A minimally perfect hash function is one that results in no collisions for a table size that equals exactly the number of elements.
	* A hash function that generates the same output for two different inputs results in a collision. 
* Two collision resolution approaches involve seperate chaining, and open addressing. 
* An important metric for hash table performance, tuning, and resizing determination is the load factor, defined as `λ=n/m`.
	* `λ` = load factor
	* `n` = number of elements
	* `m` = capacity of hashmap
* To keep our hash table efficient, we try to keep the `λ` less than some pre-defined threshold by periodically resizing when the load factor exceeds it. Additional restrictions apply depending on if a SC or OA implementation is used.
* We prefer prime numbers for the hash table sizes. This is becuase prime numbers are more likely to have a uniform distribution of remainders than a composite number. As a result, a prime number of buckets is less likely to have collisions than a composite number of buckets.

## Seperate Chaining Concepts
![HashMap-SC](./imgs/hashmaps-sc.svg)
* Uses linked-lists for collision resolution.
* One or more elements can occupy the same hash bucket/slot by storing them in a linked list.
* When we hash a key to an index, we must search the linked-list for our value to decide whether to overwite an existing node, or insert a new node. If we hash to an empty linked-list, we can insert immediately.
* When using seperate chaining, a table's load factor *can* exceed 1. This is because for a given slot, a linked list can hold any number of key/value pairs limited to memory.
* For our SC implementation, we resize whenever the load factor  `λ ≥ 1.0`. 

## Open Addressing Concepts
![HashMap-OA-Linear](./imgs/hashmaps-oa-linear.svg)
![HashMap-OA-Quadratic](./imgs/hashmaps-oa-quad.svg)
* Uses open addressing for collision resolution.
* The idea is that if we stumble upon an occupied hash entry, we can probe/skip ahead to the next available slot for insertion of our value.
* We can use one of several open adressing techniques for resolution, including linear probing, [quadratic probing](https://en.wikipedia.org/wiki/Quadratic_probing), or double hashing:
	* Linear: `i = (i_initial + j) % m`
	* Qudaratic: `i = (i_initial + j ** 2) % m`
	* Double Hashing: `i = (i_initial + j * h2(key)) % m`
		* where `i_initial = h1(key) % m`, `h1, h2` are hash functions and `j=1,2,3...`
* In general, linear probing is more susceptible to clustering. Quadratic probing is somewhere between linear and double hashing in terms of performance.
* For our OA implementation, we use quadratic probing. An example sequence using quadratic probing is as follows:
	* $H+1^{2},H+2^{2},H+3^{2},H+4^{2},...,H+k^{2}$.
* To make OA work, we rely on using 'tombstones' markers. This ensures that if we remove an element $i$ that resides on a probing path for another element $j$ farther down the table, that we'll still be able to find that element $j$ later by leaving a placeholder. 
	* Basically, tombstones give us a way to preserve the cumulative state at which time a key was inserted with probing. So long as we remember that state, we maintain our ability to retrieve our elements even after removals.
	* As an analogy, consider a squirrel🐿️ that hides its nuts🥜 in one-dimension (1D). Key/value pairs are like markers or visual cues that it uses to locate its nuts again after burying them; the markers could also represents stashes of other nuts (like in our hashmap)! If we remove, a cue (or stash of nuts) that the squirrel relied on for locating another stash of nuts, the squirrel won't be able to find its nuts again, or may even dig up the wrong nuts (that's nuts!)! So intead, we leave a little placeholder, a nut crumb trail, if you will, as a reminder. There you have it, squirrel's use hashmapping!
* A distinction compared with SC, is that two search loops are generally needed to decide whether to insert or update a value. The first search checks for the presence of the key, and if found, udpates the value. If the key is not found, then a second search is performed to find the first available slot to insert.
	* In general, the first search ignores tombstones, and terminates when an empty slot is found.
	* The second search terminates when either a tombstone or empty slot is found. 
* When using open addressing, a table’s load factor *cannot* exceed 1 because each slot can only hold one hash entry, unlike in SC which uses linked-lists, which allows us to stack values on the same lot.
* However, there are only `m/2` distinct probes for a given element, requiring other techniques to guarantee that insertions will succeed when the load factor exceeds 1/2.
* Complexity
	* In general, the probability `p` that the first probe is successful is `p=(m-n)/m`
	* There are `m` total slots and `n` filled slots, so `m − n` open spots.
	* The probability of success that the c-th probe is successful is `(m−n)/(m−c) ≥ (m−n)/m = p`. Hence it is at least `p`.
	* The expected number of probes until success is generally: `1/p = 1/((m−n)/m) = 1/(1−n/m) = 1/(1−λ)`
	* In other words, the expected number of probes for any given operation is `O(1/(1−λ))`.
	* This means if we limit the load factor to a constant and reasonably small number, our operations will be O(1) on average. 
	* For example, if we have `λ = 0.75`, then we would expect 4 probes, on average. For `λ = 0.9`, we would expect 10 probes.
* For our OA implementation, we resize whenever the load  `λ ≥ 0.5`.

## Closing
* Hash maps are up there with AVLs in terms of coolness!
* Squirrels use hashmapping!
* When I grow up (if I ever grow up), I want to be a hash table!

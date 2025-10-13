# Promptware Standard Library - Collections
# List<T>, Map<K,V>, Set<T> with Rust-inspired APIs

import stdlib.core  # For Option<T>


# ============================================================================
# List<T> - Dynamically sized array with functional operations
# ============================================================================

class List<T>:
    """
    A dynamically sized array that stores elements of type T.
    Provides efficient push/pop at the end and functional operations.
    """
    items: array<T>


# Constructors
function list_new<T>() -> List<T>:
    """
    Create an empty list.

    Returns:
        Empty List<T>

    Example:
        let todos = list_new()
    """
    return List { items: [] }


function list_from<T>(items: array<T>) -> List<T>:
    """
    Create a list from an array.

    Args:
        items: Array of items to initialize the list

    Returns:
        List<T> containing the items

    Example:
        let numbers = list_from([1, 2, 3, 4, 5])
    """
    return List { items: items }


# Core operations
function list_push<T>(lst: List<T>, item: T) -> void:
    """
    Add an item to the end of the list.
    Modifies the list in place.

    Args:
        lst: The list to modify
        item: Item to add

    Example:
        let todos = list_new()
        list_push(todos, "Write code")
        list_push(todos, "Write tests")
    """
    lst.items.append(item)


function list_pop<T>(lst: List<T>) -> Option<T>:
    """
    Remove and return the last item from the list.
    Returns None if the list is empty.

    Args:
        lst: The list to pop from

    Returns:
        Option<T> containing the last item, or None if empty

    Example:
        let items = list_from([1, 2, 3])
        let last = list_pop(items)  # Some(3)

        let empty = list_new()
        let none = list_pop(empty)  # None
    """
    if len(lst.items) == 0:
        return None
    else:
        let item = lst.items[-1]
        lst.items = lst.items[:-1]
        return Some(item)


function list_get<T>(lst: List<T>, index: int) -> Option<T>:
    """
    Get item at index, or None if out of bounds.

    Args:
        lst: The list to access
        index: Index of item to get

    Returns:
        Option<T> containing the item, or None if out of bounds

    Example:
        let items = list_from([10, 20, 30])
        let first = list_get(items, 0)  # Some(10)
        let bad = list_get(items, 99)  # None
        let negative = list_get(items, -1)  # None (negative indices not supported)
    """
    if index < 0 or index >= len(lst.items):
        return None
    else:
        return Some(lst.items[index])


function list_len<T>(lst: List<T>) -> int:
    """
    Return the number of items in the list.

    Args:
        lst: The list to measure

    Returns:
        Number of items

    Example:
        let items = list_from([1, 2, 3])
        let count = list_len(items)  # 3
    """
    return len(lst.items)


function list_is_empty<T>(lst: List<T>) -> bool:
    """
    Check if list is empty.

    Args:
        lst: The list to check

    Returns:
        true if empty, false otherwise

    Example:
        let empty = list_new()
        let check = list_is_empty(empty)  # true

        let items = list_from([1])
        let check2 = list_is_empty(items)  # false
    """
    return len(lst.items) == 0


# Functional operations
function list_map<T, U>(lst: List<T>, fn: function(T) -> U) -> List<U>:
    """
    Transform each element with a function, creating a new list.

    Args:
        lst: The list to map over
        fn: Function to apply to each element

    Returns:
        New List<U> with transformed elements

    Example:
        let numbers = list_from([1, 2, 3])
        let doubled = list_map(numbers, fn(x) -> x * 2)  # [2, 4, 6]
        let strings = list_map(numbers, fn(x) -> str(x))  # ["1", "2", "3"]
    """
    let result = []
    for item in lst.items:
        result.append(fn(item))
    return list_from(result)


function list_filter<T>(lst: List<T>, fn: function(T) -> bool) -> List<T>:
    """
    Keep only elements that match the predicate.

    Args:
        lst: The list to filter
        fn: Predicate function (returns true to keep)

    Returns:
        New List<T> with matching elements

    Example:
        let numbers = list_from([1, 2, 3, 4, 5])
        let evens = list_filter(numbers, fn(x) -> x % 2 == 0)  # [2, 4]
        let big = list_filter(numbers, fn(x) -> x > 3)  # [4, 5]
    """
    let result = []
    for item in lst.items:
        if fn(item):
            result.append(item)
    return list_from(result)


function list_fold<T, U>(lst: List<T>, init: U, fn: function(U, T) -> U) -> U:
    """
    Reduce list to a single value by accumulating with a function.
    Also known as reduce or foldl.

    Args:
        lst: The list to fold
        init: Initial accumulator value
        fn: Function that takes (accumulator, item) and returns new accumulator

    Returns:
        Final accumulated value

    Example:
        let numbers = list_from([1, 2, 3, 4])
        let sum = list_fold(numbers, 0, fn(acc, x) -> acc + x)  # 10
        let product = list_fold(numbers, 1, fn(acc, x) -> acc * x)  # 24

        let words = list_from(["hello", "world"])
        let sentence = list_fold(words, "", fn(acc, w) -> acc + " " + w)  # " hello world"
    """
    let acc = init
    for item in lst.items:
        acc = fn(acc, item)
    return acc


# ============================================================================
# Map<K,V> - Key-value store with type-safe access
# ============================================================================

class Map<K, V>:
    """
    A key-value store that maps keys of type K to values of type V.
    Provides efficient lookup, insertion, and removal.
    """
    entries: map<K, V>


# Constructors
function map_new<K, V>() -> Map<K, V>:
    """
    Create an empty map.

    Returns:
        Empty Map<K, V>

    Example:
        let config = map_new()
    """
    return Map { entries: {} }


# Core operations
function map_insert<K, V>(m: Map<K, V>, key: K, value: V) -> Option<V>:
    """
    Insert key-value pair into the map.
    Returns the old value if key already existed, None otherwise.

    Args:
        m: The map to modify
        key: The key to insert
        value: The value to associate with the key

    Returns:
        Option<V> containing old value if key existed, None if new

    Example:
        let config = map_new()
        let old = map_insert(config, "port", 8080)  # None (new key)
        let replaced = map_insert(config, "port", 9000)  # Some(8080)
    """
    let old_value = None
    if key in m.entries:
        old_value = Some(m.entries[key])
    m.entries[key] = value
    return old_value


function map_get<K, V>(m: Map<K, V>, key: K) -> Option<V>:
    """
    Get value for key, or None if not found.

    Args:
        m: The map to access
        key: The key to look up

    Returns:
        Option<V> containing the value, or None if key doesn't exist

    Example:
        let config = map_new()
        map_insert(config, "host", "localhost")

        let host = map_get(config, "host")  # Some("localhost")
        let missing = map_get(config, "port")  # None
    """
    if key in m.entries:
        return Some(m.entries[key])
    else:
        return None


function map_remove<K, V>(m: Map<K, V>, key: K) -> Option<V>:
    """
    Remove key from map and return its value.
    Returns None if key didn't exist.

    Args:
        m: The map to modify
        key: The key to remove

    Returns:
        Option<V> containing the removed value, or None if key didn't exist

    Example:
        let config = map_new()
        map_insert(config, "debug", true)

        let removed = map_remove(config, "debug")  # Some(true)
        let missing = map_remove(config, "port")  # None
    """
    if key in m.entries:
        let value = m.entries[key]
        delete m.entries[key]
        return Some(value)
    else:
        return None


function map_contains_key<K, V>(m: Map<K, V>, key: K) -> bool:
    """
    Check if key exists in the map.

    Args:
        m: The map to check
        key: The key to look for

    Returns:
        true if key exists, false otherwise

    Example:
        let config = map_new()
        map_insert(config, "host", "localhost")

        let has_host = map_contains_key(config, "host")  # true
        let has_port = map_contains_key(config, "port")  # false
    """
    return key in m.entries


function map_len<K, V>(m: Map<K, V>) -> int:
    """
    Return the number of key-value pairs in the map.

    Args:
        m: The map to measure

    Returns:
        Number of entries

    Example:
        let config = map_new()
        map_insert(config, "host", "localhost")
        map_insert(config, "port", 8080)
        let count = map_len(config)  # 2
    """
    return len(m.entries)


function map_is_empty<K, V>(m: Map<K, V>) -> bool:
    """
    Check if map is empty.

    Args:
        m: The map to check

    Returns:
        true if empty, false otherwise

    Example:
        let empty = map_new()
        let check = map_is_empty(empty)  # true

        map_insert(empty, "key", "value")
        let check2 = map_is_empty(empty)  # false
    """
    return len(m.entries) == 0


function map_keys<K, V>(m: Map<K, V>) -> List<K>:
    """
    Get list of all keys in the map.

    Args:
        m: The map to extract keys from

    Returns:
        List<K> containing all keys

    Example:
        let config = map_new()
        map_insert(config, "host", "localhost")
        map_insert(config, "port", 8080)
        let all_keys = map_keys(config)  # ["host", "port"] (order may vary)
    """
    return list_from(keys(m.entries))


function map_values<K, V>(m: Map<K, V>) -> List<V>:
    """
    Get list of all values in the map.

    Args:
        m: The map to extract values from

    Returns:
        List<V> containing all values

    Example:
        let config = map_new()
        map_insert(config, "host", "localhost")
        map_insert(config, "port", 8080)
        let all_values = map_values(config)  # ["localhost", 8080] (order may vary)
    """
    return list_from(values(m.entries))


# ============================================================================
# Set<T> - Collection of unique elements
# ============================================================================

class Set<T>:
    """
    A collection that stores unique elements of type T.
    Automatically prevents duplicates.
    """
    elements: set<T>


# Constructors
function set_new<T>() -> Set<T>:
    """
    Create an empty set.

    Returns:
        Empty Set<T>

    Example:
        let tags = set_new()
    """
    return Set { elements: set() }


# Core operations
function set_insert<T>(s: Set<T>, value: T) -> bool:
    """
    Insert value into the set.
    Returns true if value was newly inserted, false if already present.

    Args:
        s: The set to modify
        value: Value to insert

    Returns:
        true if newly inserted, false if already present

    Example:
        let tags = set_new()
        let inserted = set_insert(tags, "python")  # true
        let duplicate = set_insert(tags, "python")  # false (already exists)
    """
    if value in s.elements:
        return false
    else:
        s.elements.add(value)
        return true


function set_remove<T>(s: Set<T>, value: T) -> bool:
    """
    Remove value from the set.
    Returns true if value existed and was removed, false if not found.

    Args:
        s: The set to modify
        value: Value to remove

    Returns:
        true if removed, false if didn't exist

    Example:
        let tags = set_new()
        set_insert(tags, "python")

        let removed = set_remove(tags, "python")  # true
        let missing = set_remove(tags, "java")  # false
    """
    if value in s.elements:
        s.elements.remove(value)
        return true
    else:
        return false


function set_contains<T>(s: Set<T>, value: T) -> bool:
    """
    Check if value exists in the set.

    Args:
        s: The set to check
        value: Value to look for

    Returns:
        true if value exists, false otherwise

    Example:
        let tags = set_new()
        set_insert(tags, "python")

        let has_python = set_contains(tags, "python")  # true
        let has_java = set_contains(tags, "java")  # false
    """
    return value in s.elements


function set_len<T>(s: Set<T>) -> int:
    """
    Return the number of elements in the set.

    Args:
        s: The set to measure

    Returns:
        Number of elements

    Example:
        let tags = set_new()
        set_insert(tags, "python")
        set_insert(tags, "rust")
        let count = set_len(tags)  # 2
    """
    return len(s.elements)


function set_is_empty<T>(s: Set<T>) -> bool:
    """
    Check if set is empty.

    Args:
        s: The set to check

    Returns:
        true if empty, false otherwise

    Example:
        let empty = set_new()
        let check = set_is_empty(empty)  # true

        set_insert(empty, "item")
        let check2 = set_is_empty(empty)  # false
    """
    return len(s.elements) == 0

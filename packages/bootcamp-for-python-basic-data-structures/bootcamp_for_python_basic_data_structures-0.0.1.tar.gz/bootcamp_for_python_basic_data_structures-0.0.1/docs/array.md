# MyArray Class

The `MyArray` class is a custom implementation of an array that wraps around Python’s list, providing basic array operations such as adding, removing, updating elements, checking if the array is empty, and displaying the array's contents.

## Features

- **Add Element**: Add an element to the array.
- **Remove Element**: Remove the first occurrence of an item in the array.
- **Update Element**: Update the value of an element at a specified index.
- **Check if Empty**: Check if the array is empty.
- **Get Size**: Get the number of elements in the array.
- **Display**: Print the contents of the array.

## Methods

### `__init__(self)`
Initializes an empty `MyArray` instance.

### `add_element(self, newElement)`
Adds a new element to the end of the array.

**Arguments**:
- `newElement`: The element to be added to the array.

**Example**:
```python
my_array = MyArray()
my_array.add_element(10)
my_array.display()  # Output: [10]
```

### `remove_at(self, item)`
Removes the first occurrence of the specified item from the array.

**Arguments**:
- `item`: The item to be removed from the array.

**Returns**:
- `None` if the removal is successful. 
- Raises a `ValueError` if the item is not found in the array.

**Example**:
```python
my_array = MyArray()
my_array.add_element(10)
my_array.add_element(20)
my_array.remove_at(10)
my_array.display()  # Output: [20]
```

### `update(self, item, index)`
Updates the element at the specified index with a new value.

**Arguments**:
- `item`: The new value to place at the specified index.
- `index`: The index position to be updated.

**Returns**:
- `"index out of bound"` if the index is out of bounds.
- `None` if the update is successful.

**Example**:
```python
my_array = MyArray()
my_array.add_element(10)
my_array.add_element(20)
my_array.update(30, 1)
my_array.display()  # Output: [10, 30]
```

### `isEmpty(self)`
Checks if the array is empty.

**Returns**:
- `True` if the array is empty.
- `False` if the array is not empty.

**Example**:
```python
my_array = MyArray()
print(my_array.isEmpty())  # Output: True
my_array.add_element(10)
print(my_array.isEmpty())  # Output: False
```

### `size(self)`
Returns the current size (number of elements) of the array.

**Returns**:
- `int`: The number of elements in the array.

**Example**:
```python
my_array = MyArray()
my_array.add_element(10)
my_array.add_element(20)
print(my_array.size())  # Output: 2
```

### `display(self)`
Displays the contents of the array.

**Example**:
```python
my_array = MyArray()
my_array.add_element(10)
my_array.add_element(20)
my_array.display()  # Output: [10, 20]
```

---

## Example Usage

Here’s an example demonstrating how to use the `MyArray` class:

```python
# Create an instance of MyArray
my_array = MyArray()

# Add elements
my_array.add_element(10)
my_array.add_element(20)
my_array.add_element(30)

# Display the array
my_array.display()  # Output: [10, 20, 30]

# Remove an element
my_array.remove_at(20)
my_array.display()  # Output: [10, 30]

# Update an element
my_array.update(25, 1)
my_array.display()  # Output: [10, 25]

# Check if the array is empty
print(my_array.isEmpty())  # Output: False

# Get the size of the array
print(my_array.size())  # Output: 2
```
class Array:
    def __init__(self):
        self.array = []

    def insert(self, index: int, value):
        """Insert a value at a specified index."""
        if index < 0 or index > len(self.array):
            print("Error: Index out of bounds.")
        else:
            self.array.insert(index, value)

    def delete(self, index:int):
        """Delete the element at the specified index."""
        if index < 0 or index >= len(self.array):
            print("Error: Index out of bounds.")
        else:
            self.array.pop(index)

    def search(self, value):
        """Search for a value in the array and return its index or -1 if not found."""
        if value in self.array:
            return self.array.index(value)
        else:
            return -1

    def traverse(self):
        """Return all elements in the array."""
        return self.array

    def length(self):
        """Return the length of the array."""
        return len(self.array)

    def is_empty(self):
        """Check if the array is empty."""
        return len(self.array) == 0

    def __str__(self):
        """String representation of the array."""
        return f"Array: {self.array}"
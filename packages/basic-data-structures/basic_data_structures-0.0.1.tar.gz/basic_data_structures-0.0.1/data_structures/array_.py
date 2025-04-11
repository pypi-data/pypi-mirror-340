class MyArray:
    """
    A custom array implementation with basic array operations.
    
    This class provides a wrapper around Python's list with methods for adding,
    removing, updating elements, and checking array properties.
    """
    
    def __init__(self):
        """
        Initialize an empty MyArray instance.
        """
        self.data = []

    def add_element(self, newElement):
        """
        Add a new element to the end of the array.
        
        Args:
            newElement: The element to be added to the array.
        """
        self.data.append(newElement)

    def remove_at(self, item):
        """
        Remove the first occurrence of the specified item from the array.
        
        Args:
            item: The item to be removed from the array.
            
        Returns:
            None if successful. Raises ValueError if item is not present.
        """
        return self.data.remove(item)

    def update(self, item, index):
        """
        Update the element at the specified index with a new value.
        
        Args:
            item: The new value to place at the specified index.
            index (int): The index position to be updated.
            
        Returns:
            str: Error message if index is out of bounds.
            None: If update is successful.
        """
        if index > len(self.data) - 1:
            return "index out of bound"
        self.data[index] = item      

    def isEmpty(self):
        """
        Check if the array is empty.
        
        Returns:
            bool: True if the array is empty, False otherwise.
        """
        return len(self.data) == 0

    def size(self):
        """
        Get the current size of the array.
        
        Returns:
            int: The number of elements in the array.
        """
        return len(self.data)

    def display(self):
        """
        Print the contents of the array to the console.
        """
        print(self.data)
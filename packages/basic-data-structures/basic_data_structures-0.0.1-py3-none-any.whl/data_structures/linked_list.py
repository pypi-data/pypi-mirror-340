class Node:
    """
    A node in a singly linked list.

    Attributes:
        data: The data stored in the node.
        next: A reference to the next node in the list.
    """
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """
    A singly linked list with basic functionalities such as insertion, deletion, sorting, and searching.
    """
    def __init__(self):
        self.head = None

    def bubble_sort(self):
        """
        Sorts the linked list in ascending order using the bubble sort algorithm.
        """
        if not self.head or not self.head.next:
            return

        n = self.get_length()
        for i in range(n):
            current = self.head
            previous = None
            for j in range(n - i - 1):
                next_node = current.next
                if current.data > next_node.data:
                    if previous:
                        previous.next = next_node
                    else:
                        self.head = next_node
                    current.next = next_node.next
                    next_node.next = current
                    previous = next_node
                else:
                    previous = current
                    current = current.next
                if not current.next:
                    break

    def insertAtBeginning(self, item):
        """
        Inserts a new node with the given item at the beginning of the list.
        """
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def insertAfter(self, item, index):
        """
        Inserts a new node with the given item after the specified index.
        """
        if not self.head and index == 0:
            print("empty linked list")
            return
        i = 0
        new_node = Node(item)
        node = self.head
        while (i != (index - 1)) and node.next:
            node = node.next
            i += 1
        if node.next:
            _temp = node.next
            node.next = new_node
            new_node.next = _temp
        elif i < (index - 1):
            print("index out of bound")
        else:
            node.next = Node(item)

    def insertAtEnd(self, item):
        """
        Inserts a new node with the given item at the end of the list.
        """
        new_node = Node(item)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new_node

    def deleteItem(self, item):
        """
        Deletes the node at the specified index (1-based).
        """
        if not self.head:
            print("the list is empty")
            return
        if item == 1:
            self.head = self.head.next
            return
        temp = self.head
        count = 1
        while temp.next and count != item:
            temp_node = temp
            temp = temp.next
            count += 1
        if count == item:
            temp_node.next = temp.next
        else:
            print("index out of bound")

    def getHead(self):
        """
        Returns the head node of the linked list.
        """
        return self.head

    def get_length(self):
        """
        Returns the length of the linked list.
        """
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def search(self, item):
        """
        Returns the index of the first occurrence of the item in the list.
        """
        if not self.head:
            print("the list is empty")
            return
        temp = self.head
        index = 0
        while temp and temp.data != item:
            temp = temp.next
            index += 1
        return index if temp else -1

    def reverse(self):
        """
        Reverses the linked list.
        """
        if not self.head:
            print("the list is empty")
            return
        temp = self.head
        new_temp = LinkedList()
        while temp:
            new_temp.insertAtBeginning(temp.data)
            temp = temp.next
        self.head = new_temp.head

    def display(self):
        """
        Prints the contents of the linked list.
        """
        node = self.head
        while node:
            print(node.data, end="->")
            node = node.next
        print()

    def access(self, index):
        """
        Placeholder for accessing an item by index.
        """
        pass

    def concatenate(self, list_1):
        """
        Concatenates another linked list to the end of the current list.
        """
        if not list_1 or not self.head:
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = list_1

    def update(self, index, new_data):
        """
        Updates the data at the specified index with new data.
        """
        if not self.head:
            print("the list is empty")
            return
        temp = self.head
        i = 0
        while temp and i < index:
            temp = temp.next
            i += 1
        if temp:
            temp.data = new_data
        else:
            print("index out of bound")


class DoublyNode:
    """
    A node in a doubly linked list.

    Attributes:
        data: The data stored in the node.
        next: A reference to the next node.
        prev: A reference to the previous node.
    """
    def __init__(self, item):
        self.data = item
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    A doubly linked list implementation with various methods for manipulation.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_at_beginning(self, item):
        """
        Inserts a new node at the beginning of the list.
        """
        node = DoublyNode(item)
        if not self.head:
            self.head = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def insert_at(self, index, item):
        """
        Inserts a new node at the given index in the list.
        """
        if index != 0 and not self.head:
            print("index out of bound")
            return
        if index == 0:
            self.insert_at_beginning(item)
            return
        temp = self.head
        i = 0
        while temp.next and i < index - 1:
            temp = temp.next
            i += 1
        if i + 1 == index:
            self.insert_at_end(item)
        else:
            print("index out of bound")

    def insert_after(self, node, item):
        """
        Inserts a new node after a given node.
        """
        new_node = DoublyNode(item)
        if not node:
            node = new_node
            return
        new_node.next = node.next
        new_node.prev = node
        if node.next:
            node.next.prev = new_node
        node.next = new_node
        self.size += 1

    def insert_at_end(self, item):
        """
        Appends a new node to the end of the list.
        """
        node = DoublyNode(item)
        if not self.head:
            self.head = node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = node
            node.prev = temp
        self.size += 1

    def is_empty(self):
        """
        Checks if the list is empty.
        """
        return self.head is None

    def display(self):
        """
        Prints the contents of the doubly linked list.
        """
        node = self.head
        while node:
            print(node.data, end=" <--> ")
            node = node.next
        print('')

    def delete_item(self, key):
        """
        Deletes the node at the specified index.
        """
        if not self.head:
            print("List is empty")
            return
        if key == 0:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            self.size -= 1
            return
        current = self.head
        count = 0
        while current and count != key:
            current = current.next
            count += 1
        if not current:
            print("index out of bound")
            return
        if current.next:
            current.next.prev = current.prev
        if current.prev:
            current.prev.next = current.next
        self.size -= 1

    def search(self, item):
        """
        Returns the index of the first occurrence of item in the list.
        """
        temp = self.head
        index = 0
        while temp:
            if temp.data == item:
                return index
            temp = temp.next
            index += 1
        return -1

    def get_length(self):
        """
        Returns the number of nodes in the list.
        """
        return self.size

    def access(self, index):
        """
        Returns the data at the given index.
        """
        if not self.head:
            print("the list is empty")
            return
        if index < 0:
            print("index can not be negative")
            return
        temp = self.head
        i = 0
        while temp and i != index:
            temp = temp.next
            i += 1
        if temp:
            return temp.data
        print("index out of bound")

    def update(self, index, new_data):
        """
        Updates the data at the specified index with new_data.
        """
        temp = self.head
        i = 0
        while temp and i != index:
            temp = temp.next
            i += 1
        if temp:
            temp.data = new_data
        else:
            print("index out of bound")


    def sort(self):
        """
        Sorts the doubly linked list in ascending order using bubble sort.
        """
        if self.head is None or self.head.next is None:
            return

        end = None
        while end != self.head:
            current = self.head
            while current.next != end:
                if current.data > current.next.data:
                    current.data, current.next.data = current.next.data, current.data
                current = current.next
            end = current

    def reverse(self):
        """
        Reverses the doubly linked list in-place.
        """
        if not self.head:
            return

        current = self.head
        prev_node = None
        while current:
            # Swap next and prev
            current.prev, current.next = current.next, current.prev
            prev_node = current
            current = current.prev  # move to the next node (which is now previous)

        self.head = prev_node

class MyQueue:
    """
    A basic implementation of a fixed-size queue using a list.

    Attributes:
        size (int): Maximum number of elements the queue can hold.
        queue (list): List storing the queue elements.
    """
    def __init__(self, size, queue=None) -> None:
        """
        Initialize the queue with a fixed size.

        Args:
            size (int): Maximum capacity of the queue.
            queue (list, optional): Predefined list to use as the queue. Defaults to empty list.
        """
        self.queue = queue if queue is not None else []
        self.size = size

    def enqueue(self, newElement):
        """
        Add a new element to the end of the queue.

        Args:
            newElement: The element to be added to the queue.
        """
        if len(self.queue) == self.size:
            print("Queue is full")
        else:
            self.queue.append(newElement)

    def dequeue(self):
        """
        Remove and return the front element of the queue.

        Returns:
            The front element if available, else prints an error.
        """
        if not self.queue:
            print("Empty Queue")
        else:
            return self.queue.pop(0)

    def peek(self):
        """
        Return the front element without removing it.

        Returns:
            The front element of the queue.
        """
        if not self.queue:
            print("Empty Queue")
        else:
            return self.queue[0]

    def rear(self):
        """
        Return the last element in the queue.

        Returns:
            The rear element of the queue.
        """
        if not self.queue:
            print("Empty Queue")
        else:
            return self.queue[-1]

    def is_full(self):
        """
        Check if the queue is full.

        Returns:
            True if the queue is full, False otherwise.
        """
        return len(self.queue) == self.size

    def is_empty(self):
        """
        Check if the queue is empty.

        Returns:
            True if the queue is empty, False otherwise.
        """
        return len(self.queue) == 0

    def display(self):
        """
        Display all elements of the queue.
        """
        print(self.queue)

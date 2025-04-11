class Stack:
    """
    A simple implementation of a stack using a Python list.
    
    Attributes:
        stack (list): The list used to store stack elements.
    """
    def __init__(self, para=None):
        """
        Initializes the stack with an optional initial list.

        Args:
            para (list, optional): Initial list of elements. Defaults to an empty list.
        """
        self.stack = para if para is not None else []

    def push(self, newElement):
        """
        Push a new element onto the stack.

        Args:
            newElement: The element to be pushed.
        """
        self.stack.append(newElement)

    def pop(self):
        """
        Remove and return the top element from the stack.

        Returns:
            The top element, or a message if the stack is empty.
        """
        if not self.stack:
            return "Stack is empty"
        return self.stack.pop()

    def top(self):
        """
        Return the top element of the stack without removing it.

        Returns:
            The top element of the stack.
        """
        if not self.stack:
            return "Stack is empty"
        return self.stack[-1]

    def isEmpty(self):
        """
        Check whether the stack is empty.

        Returns:
            True if the stack is empty, False otherwise.
        """
        return len(self.stack) == 0

    def size(self):
        """
        Get the number of elements in the stack.

        Returns:
            The number of elements in the stack.
        """
        return len(self.stack)

    def display(self):
        """
        Display the current contents of the stack.
        """
        print(self.stack)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        """Insert a new node at the end of the list."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, data):
        """Delete the first occurrence of the node with the given data."""
        current = self.head
        prev = None

        while current:
            if current.data == data:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False

    def search(self, data):
        """Search for a node with the given data."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def traverse(self):
        """Return a list of all node data in the list."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def __str__(self):
        return " -> ".join(str(data) for data in self.traverse()) or "Empty"

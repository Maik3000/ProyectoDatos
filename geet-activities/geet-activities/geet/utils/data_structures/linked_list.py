'''
[Data Structure] Linked List implementation.
'''
class Node:
    def __init__(self, commit_hash, message, author, email):
        self.hash = commit_hash
        self.message = message
        self.author = author
        self.email = email
        self.next = None

class LinkedList:
    def __init__(self):
        self.start = None

    def __iter__(self):
        current = self.start
        while current:
            yield current
            current = current.next

    def traverse(self):
        current = self.start
        while current:
            print(current.hash, current.message, current.author, current.email)
            current = current.next

    def insert_first(self, node):
        node.next = self.start
        self.start = node

    def insert_last(self, node):
        if not self.start:
            self.start = node
        else:
            current = self.start
            while current.next:
                current = current.next
            current.next = node

    def remove(self, key):
        current = self.start
        previous = None
        while current:
            if current.hash == key:
                if previous:
                    previous.next = current.next
                else:
                    self.start = current.next
                return
            previous = current
            current = current.next

        print(f"Key {key} not found in the list.")

    def reverse(self):
        previous = None
        current = self.start
        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        self.start = previous

    
    
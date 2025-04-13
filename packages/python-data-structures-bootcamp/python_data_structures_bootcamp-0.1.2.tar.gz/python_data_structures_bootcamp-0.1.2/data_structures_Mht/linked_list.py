class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insertAtBeginning(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def insertAtEnd(self, item):
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def insertAfter(self, item, index):
        new_node = Node(item)
        temp = self.head
        count = 0
        while temp and count < index:
            temp = temp.next
            count += 1
        if temp is None:
            print("Index too big bro !")
        else:
            new_node.next = temp.next
            temp.next = new_node

    def deleteItem(self, index):
        if self.head is None:
            print("This list is Empty bro !")
            return

        if index == 0:
            self.head = self.head.next
            return

        temp = self.head
        count = 0
        while temp.next and count < index - 1:
            temp = temp.next
            count += 1

        if temp.next is None:
            print("Index too big bro !")
        else:
            temp.next = temp.next.next

    def display(self):
        temp = self.head
        while temp:
            print(temp.data, end = " -> ")
            temp = temp.next
        print("None")

    def search(self, item):
        temp = self.head
        index = 0
        while temp:
            if temp.data == item:
                return index
            temp = temp.next
            index += 1
        return -1

    def get_length(self):
        count = 0
        temp = self.head
        while temp:
            count += 1
            temp = temp.next
        return count

    def access(self, index):
        temp = self.head
        count = 0
        while temp and count < index:
            temp = temp.next
            count += 1
        if temp:
            return temp.data
        else:
            return "Index too big bro !"

    def update(self, index, new_data):
        temp = self.head
        count = 0
        while temp and count < index:
            temp = temp.next
            count += 1
        if temp:
            temp.data = new_data
        else:
            print("Index too big bro!")


